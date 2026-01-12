from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@main_bp.route('/compare')
def compare():
    """Página de comparación de algoritmos"""
    return render_template('compare.html')
