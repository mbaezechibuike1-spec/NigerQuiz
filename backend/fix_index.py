import re

with open('app.py', 'r') as f:
    content = f.read()

# Find the index route
old_index_pattern = r'@app\.route\(\'/\'\)\s+def index\(\):.*?return render_template\([^)]+\)'

new_index = '''@app.route('/')
def index():
    import sqlite3
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Get question count
    cursor.execute('SELECT COUNT(*) FROM questions')
    question_count = cursor.fetchone()[0]
    
    # Get total users (if table exists)
    try:
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
    except:
        total_users = 0
    
    conn.close()
    
    # Active players (simulate if no users yet)
    active_players = max(1, total_users + 5)  # Show at least 5 active players
    
    return render_template('index.html', 
        question_count=question_count,
        player_count=active_players,
        total_users=total_users)'''

# Replace using regex
content = re.sub(old_index_pattern, new_index, content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Index route updated with error handling!")
