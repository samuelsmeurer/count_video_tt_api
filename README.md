# 🚀 El Dorado P2P TikTok Analytics API

API para analisar menções "@El Dorado P2P" em vídeos do TikTok por período.

## 📡 Endpoints

### `GET /`
Documentação da API

### `GET /health` 
Health check

### `POST /analyze`
Analisar vídeos com menções "@El Dorado P2P"

**Body:**
```json
{
  "username": "cafeconleche1y2",
  "start_date": "2025-08-01", 
  "end_date": "2025-08-31"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "username": "cafeconleche1y2",
    "user_id": "6928925952189744134",
    "period": {
      "start_date": "2025-08-01",
      "end_date": "2025-08-31"
    },
    "target_mention": "@El Dorado P2P",
    "summary": {
      "total_videos_in_period": 15,
      "videos_with_mentions": 2,
      "mention_percentage": 13.33
    },
    "videos_with_mentions": [
      {
        "video_id": "7543756858041961733",
        "date": "2025-08-28",
        "description": "Hay que ayudar a tus familiares y con el @El Dorado P2P...",
        "views": 274900,
        "likes": 12651,
        "comments": 117,
        "shares": 129
      }
    ]
  }
}
```

## 🚀 Deploy no Railway

1. **Faça upload destes arquivos** para um repositório GitHub
2. **Acesse:** https://railway.app
3. **Conecte seu repositório**
4. **Configure a variável de ambiente:**
   - `RAPIDAPI_KEY` = sua chave da RapidAPI
5. **Deploy automático!**

## 🧪 Como testar

```bash
# Substitua YOUR_URL pela URL do Railway
curl -X POST https://YOUR_URL/analyze \
     -H "Content-Type: application/json" \
     -d '{
       "username": "cafeconleche1y2",
       "start_date": "2025-08-01",
       "end_date": "2025-08-31"
     }'
```

## 📁 Arquivos necessários

✅ `app.py` - API principal  
✅ `requirements.txt` - Dependências Python  
✅ `railway.json` - Configuração Railway  
✅ `Procfile` - Comando de inicialização  
✅ `.env.example` - Exemplo de variáveis de ambiente  

## 🎯 Funcionalidades

- ✅ Busca sempre por "@El Dorado P2P" nas descrições
- ✅ Filtra vídeos por período (data início/fim)
- ✅ Retorna contagem e porcentagem de menções
- ✅ Inclui detalhes dos vídeos (views, likes, etc.)
- ✅ Configurado para deploy no Railway