import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput } from 'react-react-native';

export default function MissionDetailScreen() {
  const [feedback, setFeedback] = useState<string | null>(null);

  const handleSync = async () => {
    // Dans l'app réelle, cette fonction sauvegarde localement (SQLite) 
    // puis déclenche la requête fetch('/api/v1/missions/sync') quand le réseau revient
    console.log("Enregistrement local et mise en file d'attente de synchronisation...");
  };

  return (
    <ScrollView style={styles.container}>
      {/* AI Context Section */}
      <View style={styles.aiCard}>
        <View style={styles.aiHeader}>
          <Text style={styles.aiTitle}>Prévision Intelligence Artificielle</Text>
          <Text style={styles.aiConfidence}>Confiance: 94%</Text>
        </View>
        <Text style={styles.aiPrediction}>Déforestation probable</Text>
        <Text style={styles.aiDetails}>Surface affectée: 12.4 ha | Chute NDVI: -18%</Text>
      </View>

      {/* Field Collection Section */}
      <Text style={styles.sectionTitle}>Collecte de Preuves (Hors-Ligne)</Text>
      <View style={styles.evidenceContainer}>
        <TouchableOpacity style={styles.evidenceBtn}>
          <Text style={styles.evidenceBtnText}>📷 Prendre une Photo</Text>
          <Text style={styles.evidenceSubText}>GPS & Horodatage auto.</Text>
        </TouchableOpacity>
      </View>

      {/* Human in the loop Feedback */}
      <Text style={styles.sectionTitle}>Validation Terrain (Learning Loop)</Text>
      <View style={styles.feedbackContainer}>
        <TouchableOpacity 
          style={[styles.feedbackBtn, feedback === 'Confirmé' && styles.feedbackBtnActive]}
          onPress={() => setFeedback('Confirmé')}
        >
          <Text style={[styles.feedbackText, feedback === 'Confirmé' && styles.feedbackTextActive]}>✅ Confirmé (Déforestation)</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.feedbackBtn, feedback === 'Erreur' && styles.feedbackBtnActive]}
          onPress={() => setFeedback('Erreur')}
        >
          <Text style={[styles.feedbackText, feedback === 'Erreur' && styles.feedbackTextActive]}>❌ Erreur IA (Faux positif)</Text>
        </TouchableOpacity>
      </View>

      <TextInput 
        style={styles.input} 
        placeholder="Observations supplémentaires..."
        multiline
        numberOfLines={4}
      />

      <TouchableOpacity style={styles.btnSubmit} onPress={handleSync}>
        <Text style={styles.btnSubmitText}>Valider et Synchroniser (Signé)</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC', padding: 16 },
  aiCard: { backgroundColor: '#F0FDF4', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#BBF7D0', marginBottom: 24, marginTop: 24 },
  aiHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  aiTitle: { fontSize: 12, fontWeight: 'bold', color: '#16A34A', textTransform: 'uppercase' },
  aiConfidence: { fontSize: 12, fontWeight: 'bold', color: '#15803D' },
  aiPrediction: { fontSize: 20, fontWeight: 'bold', color: '#052E16', marginBottom: 4 },
  aiDetails: { fontSize: 14, color: '#166534' },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#0F172A', marginBottom: 12 },
  evidenceContainer: { marginBottom: 24 },
  evidenceBtn: { backgroundColor: '#F1F5F9', borderStyle: 'dashed', borderWidth: 2, borderColor: '#CBD5E1', padding: 24, borderRadius: 12, alignItems: 'center' },
  evidenceBtnText: { fontSize: 16, fontWeight: 'bold', color: '#334155', marginBottom: 4 },
  evidenceSubText: { fontSize: 12, color: '#64748B' },
  feedbackContainer: { gap: 8, marginBottom: 16 },
  feedbackBtn: { backgroundColor: '#FFF', borderWidth: 1, borderColor: '#E2E8F0', padding: 16, borderRadius: 8 },
  feedbackBtnActive: { backgroundColor: '#052E16', borderColor: '#052E16' },
  feedbackText: { fontSize: 14, fontWeight: 'bold', color: '#334155' },
  feedbackTextActive: { color: '#FFF' },
  input: { backgroundColor: '#FFF', borderWidth: 1, borderColor: '#E2E8F0', borderRadius: 8, padding: 12, height: 100, textAlignVertical: 'top', marginBottom: 24 },
  btnSubmit: { backgroundColor: '#16A34A', padding: 16, borderRadius: 8, alignItems: 'center', marginBottom: 40 },
  btnSubmitText: { color: '#FFF', fontWeight: 'bold', fontSize: 16 }
});
