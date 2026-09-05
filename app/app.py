import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory

# Ajouter le répertoire racine au PYTHONPATH pour pouvoir importer src
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

app = Flask(__name__)

# Servir les fichiers de données (comme la carte folium HTML)
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(root_dir / 'data', filename)

from src.api import get_dashboard_stats

@app.route('/')
def dashboard():
    # Statistiques dynamiques issues des scripts métiers
    stats = get_dashboard_stats()
    return render_template('index.html', stats=stats)

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/zones')
def zones_page():
    return render_template('zones.html')

@app.route('/analyses')
def analyses_page():
    return render_template('analyses.html')

@app.route('/indices')
def indices_page():
    return render_template('indices.html')

@app.route('/satellites')
def satellites_page():
    return render_template('satellites.html')

@app.route('/alertes')
def alertes_page():
    return render_template('historique.html') # The previous audit page was named historique

@app.route('/comparaison')
def comparaison_page():
    # Placeholder
    stats = get_dashboard_stats()
    return render_template('index.html', stats=stats)

@app.route('/missions')
def missions_page():
    return render_template('missions.html')

@app.route('/audit')
def audit_page():
    return render_template('historique.html') # The audit page was built on historique.html

@app.route('/case-file')
def case_file_page():
    return render_template('case_file.html')

@app.route('/environnement')
def environnement_page():
    return render_template('environnement.html')

@app.route('/territory-profile')
def territory_profile_page():
    return render_template('territory_profile.html')

@app.route('/api-settings')
def api_settings_page():
    # Placeholder
    return render_template('parametres.html')

@app.route('/rapports')
def rapports_page():
    return render_template('rapports.html')

@app.route('/parametres')
def parametres_page():
    return render_template('parametres.html')

@app.route('/securite')
def securite_page():
    return render_template('securite.html')

@app.route('/integrations')
def integrations_page():
    return render_template('integrations.html')

@app.route('/predictions')
def predictions_page():
    return render_template('predictions.html')

@app.route('/digital-twin')
def digital_twin_page():
    return render_template('digital_twin.html')

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "monitored_zones": 1,
        "risk_zones": 0,
        "active_alerts": 0,
        "analyzed_images": 3
    })

@app.route('/api/trigger_download', methods=['POST'])
def trigger_download():
    import threading
    try:
        from src.download_sentinel2 import run_download
        # Lancer le téléchargement dans un thread en arrière-plan
        thread = threading.Thread(target=run_download)
        thread.daemon = True
        thread.start()
        return jsonify({"status": "accepted", "message": "Téléchargement lancé en arrière-plan."}), 202
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

from flask import request
import json

@app.route('/api/settings', methods=['GET'])
def get_settings():
    config_path = root_dir / "data" / "config.json"
    config = {
        "org_name": "GeoGuard Admin",
        "timezone": "UTC",
        "diff_threshold": 1500,
        "alert_threshold": 2.0,
        "ai_model": "v1_basic",
        "cloud_detection": True,
        "scan_frequency": "daily",
        "notification_emails": "admin@geoguard.local",
        "aws_key": "",
        "aws_secret": ""
    }
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                saved = json.load(f)
                config.update(saved)
        except: pass
        
    # Read AWS keys from .env if possible (just the key, never send secret back fully)
    env_path = root_dir / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("AWS_ACCESS_KEY_ID="):
                    config["aws_key"] = line.split("=")[1].strip()
    return jsonify(config)

@app.route('/api/settings/save', methods=['POST'])
def save_settings():
    data = request.json
    config_path = root_dir / "data" / "config.json"
    
    # Séparer les identifiants AWS des configs standards
    aws_key = data.pop("aws_key", "")
    aws_secret = data.pop("aws_secret", "")
    
    if aws_key or aws_secret:
        env_content = f"AWS_ACCESS_KEY_ID={aws_key}\nAWS_SECRET_ACCESS_KEY={aws_secret}\n"
        with open(root_dir / ".env", "w") as f:
            f.write(env_content)
            
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(data, f, indent=4)
        
    return jsonify({"status": "success"})

@app.route('/api/generate_report', methods=['POST'])
def generate_report_api():
    try:
        import subprocess
        import glob
        
        # Exécuter de manière synchrone pour la démo
        result = subprocess.run([sys.executable, str(root_dir / "src" / "main.py")], capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({"status": "error", "message": f"Erreur du script: {result.stderr}"}), 500
            
        # Trouver le rapport le plus récent
        report_files = glob.glob(str(root_dir / "data" / "reports" / "*.json"))
        if not report_files:
            return jsonify({"status": "success", "message": "Analyse terminée, mais aucun rapport trouvé."}), 200
            
        latest_report = max(report_files, key=os.path.getctime)
        with open(latest_report, 'r', encoding='utf-8') as f:
            import json
            report_data = json.load(f)
            
        summary = report_data.get("executive_summary", "Rapport généré.")
        risk = report_data.get("risk_level", "Inconnu")
        
        msg = f"RAPPORT IA TERMINE\n\nNiveau de Risque: {risk}\n\nRésumé de l'Agent: {summary}"
        return jsonify({"status": "success", "message": msg}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    msg = data.get("message", "").lower()
    
    if "salut" in msg or "bonjour" in msg:
        response = "Bonjour Directeur ! Prêt pour le briefing opérationnel. Que souhaitez-vous analyser aujourd'hui ?"
    elif "alerte" in msg or "urgence" in msg:
        response = "Nous avons actuellement <strong>6 alertes urgentes</strong>. La plus critique concerne une déforestation suspectée dans le secteur Nord. Voulez-vous que j'ouvre le dossier ?"
    elif "rapport" in msg:
        response = "Le dernier rapport environnemental a été généré ce matin. L'indice global de santé est stable (82/100). Souhaitez-vous le télécharger ?"
    elif "zone" in msg:
        response = "La zone surveillée principale (Abidjan - Forêt du Banco) présente un NDVI en baisse depuis 2 mois. Une inspection terrain est recommandée."
    else:
        response = "<strong>Analyse en cours...</strong><br/><br/>J'ai pris en compte votre demande. Je croise actuellement les données de <i>GeoVision V2</i> avec l'historique de la zone. Une anomalie spectrale est toujours sous surveillance."
        
    return jsonify({"response": response})

@app.route('/api/download_raster')
def download_raster():
    # Return anomaly visualization map as download
    file_path = root_dir / "data" / "processed" / "anomaly_map.png"
    if file_path.exists():
        return send_from_directory(file_path.parent, file_path.name, as_attachment=True)
    return jsonify({"status": "error", "message": "Fichier introuvable. Veuillez relancer l'analyse."}), 404

if __name__ == '__main__':
    import os
    env = os.getenv("FLASK_ENV", "production")
    if env == "development":
        app.run(debug=True, port=5000)
    else:
        from waitress import serve
        print("Starting production server with waitress on port 5000...")
        serve(app, host="0.0.0.0", port=5000)
