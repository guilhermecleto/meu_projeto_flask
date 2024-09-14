from flask import Flask, render_template, request, jsonify
import instaloader
import time
import random

app = Flask(__name__)

# Função para coletar dados do Instagram
def get_instagram_data(profile_name):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
        
        # Coletar informações do perfil
        profile_data = {
            'username': profile.username,
            'followers': profile.followers,
            'profile_pic_url': profile.profile_pic_url  # URL da foto de perfil
        }

        # Coletar as 10 últimas postagens
        posts_data = []
        total_likes = 0
        total_comments = 0
        post_count = 0
        total_engagement = 0

        for post in profile.get_posts():
            if post_count >= 10:
                break

            # Adicionar um delay aleatório entre 5 e 15 segundos entre requisições
            time.sleep(random.uniform(5, 15))

            # Verificar se o post é Reels para incluir visualizações, se disponível
            is_reel = post.typename == 'GraphVideo'
            views = post.video_view_count if is_reel else None

            post_info = {
                'date': post.date,
                'url': f"https://instagram.com/p/{post.shortcode}",
                'likes': post.likes,
                'comments': post.comments,
                'views': views,  # Visualizações para Reels
                'engagement': (post.likes + post.comments) / profile.followers
            }
            posts_data.append(post_info)
            total_likes += post.likes
            total_comments += post.comments
            total_engagement += post_info['engagement']
            post_count += 1

        # Calcular médias
        avg_likes = total_likes / post_count
        avg_comments = total_comments / post_count
        avg_engagement = total_engagement / post_count

        return {
            'profile': profile_data,
            'posts': posts_data,
            'averages': {
                'avg_likes': avg_likes,
                'avg_comments': avg_comments,
                'avg_engagement': avg_engagement
            }
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_profile', methods=['POST'])
def get_profile():
    profile_name = request.form['profile_name']
    data = get_instagram_data(profile_name)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
