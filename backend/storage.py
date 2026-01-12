"""SQLite-based storage for conversations."""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .database import get_connection


def create_conversation(conversation_id: str) -> Dict[str, Any]:
    """
    Create a new conversation.

    Args:
        conversation_id: Unique identifier for the conversation

    Returns:
        New conversation dict
    """
    created_at = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversations (id, title, created_at) VALUES (?, ?, ?)",
        (conversation_id, "New Conversation", created_at)
    )

    conn.commit()
    conn.close()

    return {
        "id": conversation_id,
        "created_at": created_at,
        "title": "New Conversation",
        "messages": []
    }


def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a conversation from storage.

    Args:
        conversation_id: Unique identifier for the conversation

    Returns:
        Conversation dict or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Get conversation metadata
    cursor.execute(
        "SELECT id, title, created_at FROM conversations WHERE id = ?",
        (conversation_id,)
    )

    row = cursor.fetchone()
    if row is None:
        conn.close()
        return None

    # Get all messages for this conversation
    cursor.execute(
        "SELECT role, content, stage_data FROM messages WHERE conversation_id = ? ORDER BY id",
        (conversation_id,)
    )

    messages = []
    for msg_row in cursor.fetchall():
        role = msg_row["role"]

        if role == "user":
            messages.append({
                "role": "user",
                "content": msg_row["content"]
            })
        else:  # assistant
            # Parse stage_data JSON
            stage_data = json.loads(msg_row["stage_data"]) if msg_row["stage_data"] else {}
            messages.append({
                "role": "assistant",
                "stage1": stage_data.get("stage1", []),
                "stage2": stage_data.get("stage2", []),
                "stage3": stage_data.get("stage3", {})
            })

    conn.close()

    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "title": row["title"],
        "messages": messages
    }


def list_conversations() -> List[Dict[str, Any]]:
    """
    List all conversations (metadata only).

    Returns:
        List of conversation metadata dicts
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.title,
            c.created_at,
            COUNT(m.id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.id = m.conversation_id
        GROUP BY c.id
        ORDER BY c.created_at DESC
    """)

    conversations = []
    for row in cursor.fetchall():
        conversations.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "title": row["title"],
            "message_count": row["message_count"]
        })

    conn.close()
    return conversations


def add_user_message(conversation_id: str, content: str):
    """
    Add a user message to a conversation.

    Args:
        conversation_id: Conversation identifier
        content: User message content
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if conversation exists
    cursor.execute("SELECT id FROM conversations WHERE id = ?", (conversation_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise ValueError(f"Conversation {conversation_id} not found")

    # Insert user message
    cursor.execute(
        "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (conversation_id, "user", content, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def add_assistant_message(
    conversation_id: str,
    stage1: List[Dict[str, Any]],
    stage2: List[Dict[str, Any]],
    stage3: Dict[str, Any]
):
    """
    Add an assistant message with all 3 stages to a conversation.

    Args:
        conversation_id: Conversation identifier
        stage1: List of individual model responses
        stage2: List of model rankings
        stage3: Final synthesized response
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if conversation exists
    cursor.execute("SELECT id FROM conversations WHERE id = ?", (conversation_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise ValueError(f"Conversation {conversation_id} not found")

    # Prepare stage data as JSON
    stage_data = {
        "stage1": stage1,
        "stage2": stage2,
        "stage3": stage3
    }

    # Insert assistant message
    cursor.execute(
        "INSERT INTO messages (conversation_id, role, stage_data, created_at) VALUES (?, ?, ?, ?)",
        (conversation_id, "assistant", json.dumps(stage_data), datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def update_conversation_title(conversation_id: str, title: str):
    """
    Update the title of a conversation.

    Args:
        conversation_id: Conversation identifier
        title: New title for the conversation
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE conversations SET title = ? WHERE id = ?",
        (title, conversation_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError(f"Conversation {conversation_id} not found")

    conn.commit()
    conn.close()


def delete_conversation(conversation_id: str) -> bool:
    """
    Delete a conversation from storage.

    Args:
        conversation_id: Conversation identifier

    Returns:
        True if deleted, False if not found
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Delete conversation (CASCADE will delete messages too)
    cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))

    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return deleted
