import sys
import time

def main():
    print("*" * 75)
    print("              GEOGUARD - EXECUTION DU PIPELINE COMPLET")
    print("*" * 75)
    print("\nCe script exécute toutes les étapes de manière séquentielle.\n")

    # ETAPE 1 : ACQUISITION
    print("=== ETAPE 1 : ACQUISITION DES DONNEES ===")
    from generate_mock_data import generate_mocks
    generate_mocks()
    
    time.sleep(1)

    # ETAPE 2 : DETECTION MATHEMATIQUE
    print("\n=== ETAPE 2 : DETECTION MATHEMATIQUE DE BASE ===")
    from models.change_detection import run_change_detection
    run_change_detection()
    
    time.sleep(1)

    # ETAPE 3 : EVALUATION AGENTIQUE
    print("\n=== ETAPE 3 : EVALUATION AGENTIQUE (MULTI-AGENTS) ===")
    try:
        from agents.orchestrator import AgentOrchestrator
        import json
        from pathlib import Path
        import datetime
        
        orchestrator = AgentOrchestrator()
        report = orchestrator.run_analysis()
        
        print(f"\n[Agent Rédacteur] Rapport final généré : {report.title}")
        print(f"-> Niveau de Risque : {report.risk_level}")
        print(f"-> Résumé : {report.executive_summary}")
        
        # Sauvegarde du rapport pour le tableau de bord
        report_dir = Path("data/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=4))
            
        print(f"-> Rapport sauvegardé : {report_path}")
        
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'Agent: {e}")
        
    print("\n" + "*" * 75)
    print("                 PIPELINE TERMINE AVEC SUCCES")
    print("*" * 75)

if __name__ == "__main__":
    main()
