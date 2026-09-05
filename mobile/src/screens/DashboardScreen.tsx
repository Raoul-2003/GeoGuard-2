import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-react-native';
// Note: In a real Expo project, we'd use expo-router and actual React Native components

export default function DashboardScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Tableau de Bord</Text>
        <Text style={styles.subtitle}>GeoGuard Field Ops</Text>
      </View>

      <View style={styles.kpiContainer}>
        <View style={styles.kpiCard}>
          <Text style={styles.kpiValue}>5</Text>
          <Text style={styles.kpiLabel}>Missions du jour</Text>
        </View>
        <View style={[styles.kpiCard, styles.kpiUrgent]}>
          <Text style={[styles.kpiValue, {color: '#DC2626'}]}>2</Text>
          <Text style={[styles.kpiLabel, {color: '#DC2626'}]}>Missions Urgentes</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Missions à Proximité</Text>
      
      {/* Mock Mission Card */}
      <TouchableOpacity style={styles.missionCard}>
        <View style={styles.missionHeader}>
          <Text style={styles.missionId}>MIS-2026-00245</Text>
          <View style={styles.badgeCritical}><Text style={styles.badgeText}>Critique</Text></View>
        </View>
        <Text style={styles.missionType}>Déforestation Suspectée</Text>
        <Text style={styles.missionDistance}>À 12 km (Parc National du Banco)</Text>
        
        <TouchableOpacity style={styles.btnStart}>
          <Text style={styles.btnStartText}>Démarrer la mission</Text>
        </TouchableOpacity>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC', padding: 16 },
  header: { marginBottom: 24, marginTop: 40 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#0F172A' },
  subtitle: { fontSize: 14, color: '#64748B' },
  kpiContainer: { flexDirection: 'row', gap: 16, marginBottom: 24 },
  kpiCard: { flex: 1, backgroundColor: '#FFF', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#E2E8F0' },
  kpiUrgent: { borderColor: '#FCA5A5', backgroundColor: '#FEF2F2' },
  kpiValue: { fontSize: 32, fontWeight: '900', color: '#0F172A' },
  kpiLabel: { fontSize: 12, color: '#64748B', marginTop: 4 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#0F172A', marginBottom: 16 },
  missionCard: { backgroundColor: '#FFF', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#E2E8F0', shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 10 },
  missionHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  missionId: { fontSize: 12, fontWeight: 'bold', color: '#64748B' },
  badgeCritical: { backgroundColor: '#FEE2E2', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4 },
  badgeText: { fontSize: 10, fontWeight: 'bold', color: '#DC2626', textTransform: 'uppercase' },
  missionType: { fontSize: 18, fontWeight: 'bold', color: '#0F172A', marginBottom: 4 },
  missionDistance: { fontSize: 14, color: '#64748B', marginBottom: 16 },
  btnStart: { backgroundColor: '#052E16', padding: 16, borderRadius: 8, alignItems: 'center' },
  btnStartText: { color: '#FFF', fontWeight: 'bold', fontSize: 16 }
});
