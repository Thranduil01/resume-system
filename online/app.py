"""
Flask Web 应用 - 线上部署版本
提供网页界面用于上传PDF、查看和管理简历信息
支持 OCR 和 Grok API 增强识别
仅支持文件上传模式（适合云端部署）
支持多用户数据隔离，自动清理1小时前的数据
"""
from flask import Flask, render_template, request, jsonify, session
import os
import secrets
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from database import ResumeDatabase
from pdf_parser import parse_pdf
from pdf_parser_enhanced import parse_pdf_enhanced
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Flask Session 配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # session 1小时过期

# 文件上传配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'PDF'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 限制

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = ResumeDatabase()

# 启动后台定时任务清理过期数据
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=lambda: db.clean_expired_data(hours=1),
    trigger="interval",
    minutes=10  # 每10分钟清理一次过期数据
)
scheduler.start()

def get_or_create_session_id():
    """获取或创建用户的 session ID"""
    if 'user_id' not in session:
        session['user_id'] = secrets.token_urlsafe(32)
        session.permanent = True  # 使用永久会话（实际受 PERMANENT_SESSION_LIFETIME 限制）
    return session['user_id']

def allowed_file(filename):
    """检查文件是否为允许的类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """主页"""
    # 确保用户有 session ID
    get_or_create_session_id()
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """
    上传并解析PDF文件
    接收参数：
        - files: PDF文件列表
        - use_ocr: 是否启用 OCR（默认 true）
        - grok_api_key: Grok API Key（可选）
    """
    # 检查是否有文件
    if 'files' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    # 获取额外参数
    use_ocr = request.form.get('use_ocr', 'true').lower() == 'true'
    grok_api_key = request.form.get('grok_api_key', None)
    if grok_api_key == '':
        grok_api_key = None
    
    # 保存上传的文件
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append(filepath)
    
    if not uploaded_files:
        return jsonify({'error': '没有有效的PDF文件'}), 400
    
    # 解析PDF文件
    results, success_count, error_count = process_pdf_files(
        uploaded_files, use_ocr, grok_api_key
    )
    
    # 清理上传的临时文件
    for filepath in uploaded_files:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"清理临时文件失败: {filepath}, 错误: {str(e)}")
    
    return jsonify({
        'success': True,
        'message': f'成功解析 {success_count} 个文件，失败 {error_count} 个',
        'total': len(uploaded_files),
        'success_count': success_count,
        'error_count': error_count,
        'results': results
    })

def process_pdf_files(pdf_files, use_ocr, grok_api_key):
    """
    处理PDF文件的通用函数
    返回: (results, success_count, error_count)
    """
    results = []
    success_count = 0
    error_count = 0
    
    for pdf_path in pdf_files:
        try:
            filename = os.path.basename(pdf_path)
            
            # 使用增强版解析器
            parsed_data, method = parse_pdf_enhanced(
                pdf_path, 
                use_ocr=use_ocr,
                grok_api_key=grok_api_key if grok_api_key else None
            )
            
            # 获取当前用户的 session ID
            session_id = get_or_create_session_id()
            
            # 存入数据库（关联到用户）
            resume_id = db.insert_resume(
                session_id=session_id,
                filename=filename,
                name=parsed_data['name'],
                email=parsed_data['email'],
                undergraduate_school=parsed_data['undergraduate_school'],
                graduate_school=parsed_data['graduate_school'],
                current_grade=parsed_data['current_grade']
            )
            
            results.append({
                'filename': filename,
                'status': 'success',
                'method': method,
                'data': {
                    'name': parsed_data['name'],
                    'email': parsed_data['email'],
                    'undergraduate_school': parsed_data['undergraduate_school'],
                    'graduate_school': parsed_data['graduate_school'],
                    'current_grade': parsed_data['current_grade']
                }
            })
            success_count += 1
            
        except Exception as e:
            results.append({
                'filename': os.path.basename(pdf_path),
                'status': 'error',
                'error': str(e)
            })
            error_count += 1
    
    return results, success_count, error_count

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """获取当前用户的简历数据"""
    session_id = get_or_create_session_id()
    resumes = db.get_resumes_by_session(session_id)
    return jsonify({
        'success': True,
        'resumes': resumes
    })

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """获取当前用户的邮箱（去重）"""
    session_id = get_or_create_session_id()
    emails = db.get_emails_by_session(session_id)
    return jsonify({
        'success': True,
        'emails': emails,
        'count': len(emails)
    })

@app.route('/api/clear', methods=['POST'])
def clear_database():
    """清空当前用户的数据"""
    try:
        session_id = get_or_create_session_id()
        db.clear_by_session(session_id)
        return jsonify({
            'success': True,
            'message': '数据已清空'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/delete/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """删除指定简历（仅限当前用户的数据）"""
    try:
        session_id = get_or_create_session_id()
        db.delete_resume(resume_id, session_id)
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 支持云平台的动态端口配置
    import os
    port = int(os.environ.get('PORT', 5001))
    
    print("=" * 50)
    print("简历信息提取系统（线上版）已启动")
    print(f"请在浏览器中访问: http://127.0.0.1:{port}")
    print("💡 用户数据隔离已启用，数据将在1小时后自动清理")
    print("=" * 50)
    
    # 根据环境决定是否开启 debug
    # 生产环境（有 PORT 环境变量）关闭 debug
    is_production = 'PORT' in os.environ
    
    try:
        app.run(debug=not is_production, host='0.0.0.0', port=port)
    finally:
        # 关闭定时任务
        scheduler.shutdown()


