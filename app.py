#!/usr/bin/env python3
"""
API Railway para análise de menções @El Dorado P2P em vídeos do TikTok
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import re
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite CORS para acesso de outros domínios

class TikTokAnalyzer:
    def __init__(self, rapidapi_key):
        self.rapidapi_key = rapidapi_key
        self.headers = {
            "X-RapidAPI-Host": "scraptik.p.rapidapi.com",
            "X-RapidAPI-Key": rapidapi_key
        }
    
    def get_user_id_from_username(self, username):
        """Get user ID from username"""
        url = "https://scraptik.p.rapidapi.com/username-to-id"
        params = {"username": username}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            result = response.json()
            
            if 'uid' in result:
                return result['uid']
            elif 'user_id' in result:
                return result['user_id']
            elif 'data' in result and 'user_id' in result['data']:
                return result['data']['user_id']
            else:
                return None
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
    
    def get_user_posts(self, user_id):
        """Get user posts"""
        url = "https://scraptik.p.rapidapi.com/user-posts"
        params = {
            "user_id": user_id,
            "region": "GB"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting posts: {e}")
            return None
    
    def analyze_videos(self, username, start_date, end_date):
        """
        Analyze videos for @El Dorado P2P mentions
        """
        target_mention = "@El Dorado P2P"
        
        # Get user ID
        user_id = self.get_user_id_from_username(username)
        if not user_id:
            return {
                "success": False,
                "error": f"Usuário @{username} não encontrado"
            }
        
        # Get posts
        posts_data = self.get_user_posts(user_id)
        if not posts_data:
            return {
                "success": False,
                "error": "Erro ao buscar posts"
            }
        
        videos = posts_data.get('aweme_list', [])
        
        # Parse dates
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {
                "success": False,
                "error": "Formato de data inválido. Use YYYY-MM-DD"
            }
        
        # Analyze videos
        videos_no_periodo = 0
        videos_com_mencao = 0
        videos_detalhes = []
        
        for video in videos:
            timestamp = video.get('create_time')
            if not timestamp:
                continue
            
            try:
                video_date = datetime.fromtimestamp(int(timestamp))
                
                # Check if video is in date range
                if start_dt <= video_date <= end_dt:
                    videos_no_periodo += 1
                    
                    # Check for mention
                    description = video.get('desc', '')
                    mentions_found = False
                    
                    # Check description
                    if target_mention.lower() in description.lower():
                        mentions_found = True
                    
                    # Check text_extra for @mentions
                    if not mentions_found:
                        text_extra = video.get('text_extra', [])
                        for text_item in text_extra:
                            if text_item.get('type') == 1:
                                hashtag_name = text_item.get('hashtag_name', '')
                                if target_mention.replace('@', '').lower() in hashtag_name.lower():
                                    mentions_found = True
                                    break
                    
                    if mentions_found:
                        videos_com_mencao += 1
                        stats = video.get('statistics', {})
                        videos_detalhes.append({
                            'video_id': video.get('aweme_id'),
                            'date': video_date.strftime('%Y-%m-%d'),
                            'description': description,
                            'views': stats.get('play_count', 0),
                            'likes': stats.get('digg_count', 0),
                            'comments': stats.get('comment_count', 0),
                            'shares': stats.get('share_count', 0)
                        })
            except Exception as e:
                continue
        
        # Calculate percentage
        percentage = round((videos_com_mencao / videos_no_periodo * 100) if videos_no_periodo > 0 else 0, 2)
        
        return {
            "success": True,
            "data": {
                "username": username,
                "user_id": user_id,
                "period": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "target_mention": target_mention,
                "summary": {
                    "total_videos_in_period": videos_no_periodo,
                    "videos_with_mentions": videos_com_mencao,
                    "mention_percentage": percentage
                },
                "videos_with_mentions": videos_detalhes
            }
        }

# Initialize analyzer
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '0d944ab837msh8447eb16f435d8ep1ed7fejsn24f790dc0bb4')
analyzer = TikTokAnalyzer(RAPIDAPI_KEY)

@app.route('/', methods=['GET'])
def home():
    """API Documentation"""
    return jsonify({
        "service": "El Dorado P2P TikTok Analytics API",
        "version": "1.0",
        "description": "API para analisar menções @El Dorado P2P em vídeos do TikTok",
        "endpoints": {
            "GET /": "Documentação da API",
            "GET /health": "Health check",
            "POST /analyze": "Analisar vídeos de um usuário em um período"
        },
        "usage": {
            "endpoint": "POST /analyze",
            "parameters": {
                "username": "Nome do usuário do TikTok (obrigatório)",
                "start_date": "Data de início YYYY-MM-DD (obrigatório)",
                "end_date": "Data de fim YYYY-MM-DD (obrigatório)"
            },
            "example": {
                "username": "cafeconleche1y2",
                "start_date": "2025-08-01",
                "end_date": "2025-08-31"
            }
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "El Dorado P2P Analytics API"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze TikTok videos for @El Dorado P2P mentions
    
    Body:
    {
        "username": "cafeconleche1y2",
        "start_date": "2025-08-01",
        "end_date": "2025-08-31"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Campo obrigatório ausente: {field}"
                }), 400
        
        # Validate date format
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, data['start_date']) or not re.match(date_pattern, data['end_date']):
            return jsonify({
                "success": False,
                "error": "Formato de data inválido. Use YYYY-MM-DD"
            }), 400
        
        # Run analysis
        result = analyzer.analyze_videos(
            username=data['username'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)