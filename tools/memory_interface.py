import sqlite3

dbName = "memory.db"

def get_connection():
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT,
        filename TEXT,
        format TEXT,
        intent TEXT,
        extracted_info TEXT,
        agent TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    return conn, cursor

def log_to_memory(conversation_id, filename, format, intent, extracted_info, agent):
    conn, cursor = get_connection()
    cursor.execute("""
    INSERT INTO memory (conversation_id, filename, format, intent, extracted_info, agent)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (
        conversation_id,
        filename,
        format,
        intent,
        extracted_info,
        agent
    ))
    conn.commit()
    conn.close()

def read_logs(conversation_id):
    conn, cursor = get_connection()
    if conversation_id:
        cursor.execute("""
        SELECT * FROM memory WHERE conversation_id = ?;
        """, (conversation_id,))
    else:
        cursor.execute("""
        SELECT * FROM memory;
        """)
    logs = cursor.fetchall()
    conn.close()
    return logs

def print_logs(conversation_id=None):
    logs = read_logs(conversation_id)
    for log in logs:
         print(f"[{log[-1]}] ({log[1]}) {log[5]} | {log[3]} -> {log[4]} [{log[6]}]")

if __name__ == '__main__':
        import sys
        conv_id = sys.argv[1] if len(sys.argv) > 1 else None
        print_logs(conv_id)