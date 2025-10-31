"""
数据库模型和操作
使用 SQLite 存储简历信息
支持多用户数据隔离和自动清理
"""
import sqlite3
from datetime import datetime, timedelta
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
                session_id TEXT NOT NULL,
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
        
        # 创建索引提高查询性能
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_id 
            ON resumes(session_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON resumes(created_at)
        """)
        
        conn.commit()
        conn.close()
    
    def insert_resume(self, session_id: str, filename: str, name: Optional[str],
                     email: Optional[str], 
                     undergraduate_school: Optional[str], 
                     graduate_school: Optional[str],
                     current_grade: Optional[str]) -> int:
        """插入一条简历记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO resumes (session_id, filename, name, email, 
                               undergraduate_school, graduate_school, current_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, filename, name, email, undergraduate_school, 
              graduate_school, current_grade))
        
        resume_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return resume_id
    
    def get_resumes_by_session(self, session_id: str) -> List[Dict]:
        """获取指定用户的所有简历记录"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, name, email, undergraduate_school, 
                   graduate_school, current_grade, created_at
            FROM resumes
            WHERE session_id = ?
            ORDER BY created_at DESC
        """, (session_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_emails_by_session(self, session_id: str) -> List[str]:
        """获取指定用户的所有邮箱（去重且非空）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT email
            FROM resumes
            WHERE session_id = ? 
              AND email IS NOT NULL 
              AND email != ''
            ORDER BY email
        """, (session_id,))
        
        emails = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return emails
    
    def clear_by_session(self, session_id: str):
        """清空指定用户的所有记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resumes WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
    
    def delete_resume(self, resume_id: int, session_id: str):
        """删除指定记录（需验证是否属于该用户）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM resumes 
            WHERE id = ? AND session_id = ?
        """, (resume_id, session_id))
        conn.commit()
        conn.close()
    
    def clean_expired_data(self, hours: int = 1):
        """清理超过指定小时数的数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 计算过期时间
        expire_time = datetime.now() - timedelta(hours=hours)
        
        cursor.execute("""
            DELETE FROM resumes 
            WHERE created_at < ?
        """, (expire_time,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_session_count(self, session_id: str) -> int:
        """获取指定用户的记录数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM resumes 
            WHERE session_id = ?
        """, (session_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    # 保留旧方法用于向后兼容（管理员功能）
    def get_all_resumes(self) -> List[Dict]:
        """获取所有简历记录（仅管理员使用）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, session_id, filename, name, email, undergraduate_school, 
                   graduate_school, current_grade, created_at
            FROM resumes
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_all_emails(self) -> List[str]:
        """获取所有邮箱（仅管理员使用）"""
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
        """清空所有记录（仅管理员使用）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resumes")
        conn.commit()
        conn.close()

