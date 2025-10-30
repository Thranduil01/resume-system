"""
数据库模型和操作
使用 SQLite 存储简历信息
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class ResumeDatabase:
    def __init__(self, db_path: str = "resumes.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                name TEXT,
                email TEXT,
                undergraduate_school TEXT,
                graduate_school TEXT,
                current_grade TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_resume(self, filename: str, name: Optional[str],
                     email: Optional[str], 
                     undergraduate_school: Optional[str], 
                     graduate_school: Optional[str],
                     current_grade: Optional[str]) -> int:
        """插入一条简历记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO resumes (filename, name, email, undergraduate_school, 
                               graduate_school, current_grade)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (filename, name, email, undergraduate_school, graduate_school, current_grade))
        
        resume_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return resume_id
    
    def get_all_resumes(self) -> List[Dict]:
        """获取所有简历记录"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, name, email, undergraduate_school, 
                   graduate_school, current_grade, created_at
            FROM resumes
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_all_emails(self) -> List[str]:
        """获取所有邮箱（去重且非空）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT email
            FROM resumes
            WHERE email IS NOT NULL AND email != ''
            ORDER BY email
        """)
        
        emails = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return emails
    
    def clear_all(self):
        """清空所有记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resumes")
        conn.commit()
        conn.close()
    
    def delete_resume(self, resume_id: int):
        """删除指定记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        conn.commit()
        conn.close()

