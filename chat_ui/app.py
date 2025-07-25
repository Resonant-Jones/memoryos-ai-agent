from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import subprocess
import json
import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from services.llm import get_llm_provider
import config
import database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, database.get_user_by_id(user_id)[1])


# --- MCP Client ---
mcp_clients = {}
mcp_sessions = {}
llm_provider = None

async def start_mcp_client(user_id):
    global llm_provider
    if not llm_provider:
        llm_provider = get_llm_provider(
            config.LLM_PROVIDER,
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL
        )

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["../memoryos-mcp/server_new.py", "--config", f"../memoryos-mcp/config_{user_id}.json"],
        env=None
    )

    # Create a user-specific config file
    with open("../memoryos-mcp/config.json", "r") as f:
        base_config = json.load(f)
    base_config["user_id"] = user_id
    with open(f"../memoryos-mcp/config_{user_id}.json", "w") as f:
        json.dump(base_config, f)

    mcp_client = stdio_client(server_params)
    read_stream, write_stream = await mcp_client.__aenter__()
    mcp_session = ClientSession(read_stream, write_stream)
    await mcp_session.initialize()
    mcp_clients[user_id] = mcp_client
    mcp_sessions[user_id] = mcp_session

async def stop_mcp_client(user_id):
    if user_id in mcp_clients:
        await mcp_clients[user_id].__aexit__(None, None, None)
        del mcp_clients[user_id]
        del mcp_sessions[user_id]

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = database.get_user(username)
        if user_data and user_data[0][2] == password:
            user = User(id=user_data[0][0], username=user_data[0][1])
            login_user(user)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_mcp_client(user.id))

            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.get_user(username):
            flash('Username already exists')
        else:
            user_id = database.add_user(username, password)
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stop_mcp_client(user_id))
    return redirect(url_for('login'))


@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message')
    user_id = current_user.id
    mcp_session = mcp_sessions.get(user_id)
    if not mcp_session:
        return jsonify({'response': 'Error: Not connected to MemoryOS. Please login again.'})


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # --- Retrieve memory ---
    retrieve_result = loop.run_until_complete(mcp_session.call_tool(
        "retrieve_memory",
        {"query": user_message}
    ))

    retrieved_content = retrieve_result.content[0].text
    retrieved_data = json.loads(retrieved_content)

    # --- Generate response ---
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # Add retrieved memories to the context
    if retrieved_data.get("short_term_memory"):
        for mem in retrieved_data["short_term_memory"]:
            messages.append({"role": "user", "content": mem["user_input"]})
            messages.append({"role": "assistant", "content": mem["agent_response"]})

    messages.append({"role": "user", "content": user_message})

    bot_response = llm_provider.generate_response(messages)

    # --- Add memory ---
    loop.run_until_complete(mcp_session.call_tool(
        "add_memory",
        {
            "user_input": user_message,
            "agent_response": bot_response
        }
    ))

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    database.setup_database()
    app.run(debug=True, port=5001)
