import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function Carte() {
  return (
    <View style={styles.container}>
      <View style={styles.mapMockup}>
        {/* Lignes de quadrillage tactique simulées */}
        <View style={styles.gridLineV} />
        <View style={styles.gridLineH} />
        
        {/* Marqueur Agent (Bleu) */}
        <View style={[styles.markerAgent, { top: '40%', left: '30%' }]} />
        <View style={[styles.markerAgent, { top: '60%', left: '70%' }]} />
        
        {/* Marqueur Alerte (Rouge Pulse) */}
        <View style={[styles.markerAlertPulse, { top: '45%', left: '50%' }]} />
        <View style={[styles.markerAlert, { top: '45%', left: '50%' }]} />
        
        <View style={styles.mapOverlay}>
          <Text style={styles.overlayTitle}>Secteur Banco - Risque Élevé</Text>
          <Text style={styles.overlaySubtitle}>2 Missions en cours</Text>
        </View>
      </View>
      
      {/* Outils de la carte */}
      <View style={styles.toolsContainer}>
        <TouchableOpacity style={styles.toolButtonActive}>
          <Text style={styles.toolTextActive}>Situation Actuelle</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.toolButton}>
          <Text style={styles.toolText}>Évolution (1 an)</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.toolButton}>
          <Text style={styles.toolText}>Filtres (IA)</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#052E16' }, // Dark tactique
  mapMockup: { flex: 1, position: 'relative', overflow: 'hidden' },
  gridLineV: { position: 'absolute', width: 1, height: '100%', backgroundColor: 'rgba(255,255,255,0.05)', left: '50%' },
  gridLineH: { position: 'absolute', height: 1, width: '100%', backgroundColor: 'rgba(255,255,255,0.05)', top: '50%' },
  
  markerAgent: { position: 'absolute', width: 16, height: 16, backgroundColor: '#3B82F6', borderRadius: 8, borderWidth: 2, borderColor: 'white' },
  markerAlert: { position: 'absolute', width: 24, height: 24, backgroundColor: '#DC2626', borderRadius: 12, borderWidth: 3, borderColor: 'white', transform: [{translateX: -12}, {translateY: -12}] },
  markerAlertPulse: { position: 'absolute', width: 48, height: 48, backgroundColor: 'rgba(220,38,38,0.3)', borderRadius: 24, transform: [{translateX: -24}, {translateY: -24}] },
  
  mapOverlay: { position: 'absolute', top: 20, left: 20, right: 20, backgroundColor: 'rgba(255,255,255,0.95)', padding: 16, borderRadius: 12 },
  overlayTitle: { fontSize: 16, fontWeight: 'bold', color: '#0F172A' },
  overlaySubtitle: { fontSize: 12, color: '#64748B', marginTop: 4 },
  
  toolsContainer: { backgroundColor: 'white', padding: 20, paddingBottom: 40, flexDirection: 'row', justifyContent: 'space-between', borderTopWidth: 1, borderColor: '#E2E8F0' },
  toolButtonActive: { backgroundColor: '#16A34A', paddingVertical: 10, paddingHorizontal: 16, borderRadius: 20 },
  toolTextActive: { color: 'white', fontWeight: 'bold', fontSize: 12 },
  toolButton: { backgroundColor: '#F1F5F9', paddingVertical: 10, paddingHorizontal: 16, borderRadius: 20 },
  toolText: { color: '#64748B', fontWeight: 'bold', fontSize: 12 }
});
