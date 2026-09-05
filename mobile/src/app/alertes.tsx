import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';

export default function Alertes() {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.pageTitle}>Alertes à valider (3)</Text>
      
      {/* Alerte 1 (Détail) */}
      <View style={styles.alertDetailCard}>
        <View style={styles.alertHeader}>
          <View style={styles.alertBadgeError}><Text style={styles.alertBadgeText}>CRITIQUE</Text></View>
          <Text style={styles.timeText}>Il y a 10 min</Text>
        </View>
        
        <Text style={styles.alertTitle}>Perte végétale détectée</Text>
        <Text style={styles.alertLocation}>📍 Parc National du Banco (Secteur Est)</Text>
        
        <View style={styles.aiBox}>
          <Text style={styles.aiBoxTitle}>Analyse IA (GeoVision V2)</Text>
          <Text style={styles.aiBoxText}>Changement spectral NDVI sévère sur 12.5 hectares. Probabilité d'exploitation forestière illégale.</Text>
          <View style={styles.aiConfidenceBar}>
            <View style={[styles.aiConfidenceFill, { width: '94%' }]} />
          </View>
          <Text style={styles.aiConfidenceText}>Confiance IA: 94%</Text>
        </View>

        <View style={styles.recommendationBox}>
          <Text style={styles.recommendationTitle}>Recommandation Stratégique</Text>
          <Text style={styles.recommendationText}>Déploiement immédiat de l'Équipe Alpha (actuellement à 12km) pour inspection visuelle.</Text>
        </View>

        <View style={styles.actionGrid}>
          <TouchableOpacity style={styles.btnPrimary}>
            <Text style={styles.btnPrimaryText}>✓ Autoriser Intervention</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.btnSecondary}>
            <Text style={styles.btnSecondaryText}>Demander Analyse Expert</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.btnSecondary}>
            <Text style={styles.btnSecondaryText}>Ignorer (Faux Positif)</Text>
          </TouchableOpacity>
        </View>
      </View>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC' },
  content: { padding: 20, paddingBottom: 40 },
  
  pageTitle: { fontSize: 20, fontWeight: 'bold', color: '#0F172A', marginBottom: 20 },
  
  alertDetailCard: { backgroundColor: 'white', borderRadius: 16, padding: 20, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 10, elevation: 3, borderWidth: 1, borderColor: '#E2E8F0' },
  alertHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  alertBadgeError: { backgroundColor: '#FEE2E2', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 6, borderWidth: 1, borderColor: '#FCA5A5' },
  alertBadgeText: { fontSize: 10, fontWeight: 'bold', color: '#DC2626' },
  timeText: { fontSize: 12, color: '#64748B', fontWeight: 'bold' },
  
  alertTitle: { fontSize: 22, fontWeight: 'bold', color: '#0F172A', marginBottom: 8 },
  alertLocation: { fontSize: 14, color: '#64748B', marginBottom: 20, fontWeight: '600' },
  
  aiBox: { backgroundColor: '#F1F5F9', borderRadius: 12, padding: 16, marginBottom: 16 },
  aiBoxTitle: { fontSize: 12, fontWeight: 'bold', color: '#0F172A', textTransform: 'uppercase', marginBottom: 8 },
  aiBoxText: { fontSize: 14, color: '#475569', lineHeight: 20, marginBottom: 12 },
  aiConfidenceBar: { height: 6, backgroundColor: '#E2E8F0', borderRadius: 3, marginBottom: 8, overflow: 'hidden' },
  aiConfidenceFill: { height: '100%', backgroundColor: '#16A34A', borderRadius: 3 },
  aiConfidenceText: { fontSize: 12, fontWeight: 'bold', color: '#16A34A', textAlign: 'right' },
  
  recommendationBox: { backgroundColor: '#F0FDF4', borderRadius: 12, padding: 16, marginBottom: 24, borderWidth: 1, borderColor: '#BBF7D0' },
  recommendationTitle: { fontSize: 12, fontWeight: 'bold', color: '#16A34A', textTransform: 'uppercase', marginBottom: 8 },
  recommendationText: { fontSize: 14, color: '#166534', lineHeight: 20, fontWeight: '500' },
  
  actionGrid: { gap: 10 },
  btnPrimary: { backgroundColor: '#16A34A', padding: 16, borderRadius: 12, alignItems: 'center', shadowColor: '#16A34A', shadowOpacity: 0.2, shadowRadius: 5, elevation: 2 },
  btnPrimaryText: { color: 'white', fontWeight: 'bold', fontSize: 16 },
  btnSecondary: { backgroundColor: 'white', padding: 16, borderRadius: 12, alignItems: 'center', borderWidth: 1, borderColor: '#CBD5E1' },
  btnSecondaryText: { color: '#0F172A', fontWeight: 'bold', fontSize: 14 },
});
