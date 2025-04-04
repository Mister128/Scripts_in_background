import sqlite3 as sql
import psutil
import os

def add(name, script_path, start_by):
    script = name, script_path, start_by
    conn = sql.connect('scripts.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO scripts (name, script_path, start_by) VALUES (?, ?, ?)", script)
        conn.commit()
        conn.close()
    except sql.IntegrityError:
        return "You already had this name"

def delete(name):
    conn = sql.connect('scripts.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM scripts WHERE name = ?", (name,))
        conn.commit()
        conn.close()
    except sql.Error:
        return "There is no such name"
        

def get_scripts():
    conn = sql.connect('scripts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM scripts")
    scripts = cursor.fetchall()
    scripts = [(row[0]) for row in scripts]
    conn.close()
    return scripts

def get_script(name):
    conn = sql.connect('scripts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scripts WHERE name = ?", (name,))
    script = cursor.fetchall()
    script = [item for row in script for item in row]
    conn.close()
    return script
 
 
def get_pid_by_process_path(process_path):
        """ Функция для поиска PID процесса по его командной строке. :param command_line: Командная строка процесса. :return: PID процесса или None, если процесс не найден. """
        for proc in psutil.process_iter(['cmdline']):
            try:
                if proc.cmdline() and ' '.join(proc.cmdline()) == process_path:
                    return proc.pid
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
        return None

def get_start_by(path):
    extension = os.path.splitext(path)[1]
    program_map = {
        '.exe': 'start',
        '.dll': 'start',
        '.msi': 'start',
        '.bat': 'start',
        '.cmd': 'start',
        '.ps1': 'powershell',
        '.vbs': 'cscript',
        '.jar': 'java -jar',
        '.php': 'php',
        '.ahk': 'AutoHotkey.exe',
        '.lua': 'lua',
        '.js': 'node',
        '.py': 'python',
        '.rb': 'ruby',
        '.pl': 'perl',
        '.sh': 'bash',
        '.go': 'go build',
        '.rs': 'rustc',
        '.c': 'gcc',
        '.cpp': 'gcc',
        '.R': 'Rscript',
        '.m': 'octave',
    }
    
    program = program_map.get(extension)
    return program
    
    