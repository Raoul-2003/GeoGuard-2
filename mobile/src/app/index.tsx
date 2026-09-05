import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';

export default function Home() {
  const router = useRouter();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      
      {/* HEADER GREETING */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Bonjour, Directeur</Text>
        <Text style={styles.date}>4 Septembre 2026</Text>
      </View>

      {/* DAILY BRIEFING IA */}
      <View style={styles.briefCard}>
        <View style={styles.briefHeader}>
          <View style={styles.aiBadge}><Text style={styles.aiBadgeText}>IA</Text></View>
          <Text style={styles.briefTitle}>GeoGuard Daily Brief</Text>
        </View>
        <Text style={styles.briefText}>
          Durant les dernières 24 heures :{"\n"}
          • 12 nouvelles anomalies détectées.{"\n"}
          • 3 zones nécessitent une attention immédiate.{"\n"}
          • Le risque global a augmenté de 4%.
        </Text>
        <TouchableOpacity style={styles.briefButton}>
          <Text style={styles.briefButtonText}>Voir le rapport détaillé</Text>
        </TouchableOpacity>
      </View>

      {/* 4 KPIs STRATÉGIQUES */}
      <View style={styles.kpiGrid}>
        <View style={styles.kpiCard}>
          <Text style={styles.kpiLabel}>Risque territorial</Text>
          <Text style={styles.kpiValueError}>72<Text style={styles.kpiSuffix}>/100</Text></Text>
        </View>
        <View style={styles.kpiCard}>
          <Text style={styles.kpiLabel}>Alertes critiques</Text>
          <Text style={styles.kpiValueError}>12</Text>
        </View>
        <View style={styles.kpiCard}>
          <Text style={styles.kpiLabel}>Missions actives</Text>
          <Text style={styles.kpiValueInfo}>24</Text>
        </View>
        <View style={styles.kpiCard}>
          <Text style={styles.kpiLabel}>Évolution (NDVI)</Text>
          <Text style={styles.kpiValueError}>-5%</Text>
        </View>
      </View>

      {/* ALERTES PRIORITAIRES */}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Alertes Prioritaires (Top 3)</Text>
        <TouchableOpacity onPress={() => router.push('/alertes')}><Text style={styles.seeAll}>Voir tout</Text></TouchableOpacity>
      </View>

      <View style={styles.alertsList}>
        
        <View style={styles.alertCard}>
          <View style={styles.alertTop}>
            <View style={styles.alertBadgeError}><Text style={styles.alertBadgeText}>CRITIQUE</Text></View>
            <Text style={styles.alertConfidence}>IA: 95%</Text>
          </View>
          <Text style={styles.alertType}>Déforestation Probable</Text>
          <Text style={styles.alertZone}>Parc National du Banco</Text>
          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionButtonText}>Autoriser Intervention</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.alertCard}>
          <View style={styles.alertTop}>
            <View style={styles.alertBadgeWarning}><Text style={styles.alertBadgeText}>HAUTE</Text></View>
            <Text style={styles.alertConfidence}>IA: 88%</Text>
          </View>
          <Text style={styles.alertType}>Départ de Feu</Text>
          <Text style={styles.alertZone}>Forêt de Taï (Secteur Nord)</Text>
          <TouchableOpacity style={styles.actionButtonSecondary}>
            <Text style={styles.actionButtonTextSecondary}>Voir l'analyse</Text>
          </TouchableOpacity>
        </View>

      </View>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC' },
  content: { padding: 20, paddingBottom: 40 },
  
  header: { marginBottom: 20 },
  greeting: { fontSize: 24, fontWeight: 'bold', color: '#0F172A' },
  date: { fontSize: 14, color: '#64748B', marginTop: 4 },
  
  briefCard: { backgroundColor: '#052E16', borderRadius: 16, padding: 20, marginBottom: 24, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 10, elevation: 5 },
  briefHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  aiBadge: { backgroundColor: '#16A34A', paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4, marginRight: 8 },
  aiBadgeText: { color: 'white', fontSize: 10, fontWeight: 'bold' },
  briefTitle: { color: 'white', fontSize: 16, fontWeight: 'bold' },
  briefText: { color: 'rgba(255,255,255,0.9)', fontSize: 14, lineHeight: 22, marginBottom: 16 },
  briefButton: { backgroundColor: 'rgba(255,255,255,0.1)', padding: 12, borderRadius: 8, alignItems: 'center' },
  briefButtonText: { color: 'white', fontWeight: 'bold', fontSize: 14 },
  
  kpiGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: 24 },
  kpiCard: { width: '48%', backgroundColor: 'white', borderRadius: 12, padding: 16, marginBottom: 16, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 5, elevation: 2, borderWidth: 1, borderColor: '#E2E8F0' },
  kpiLabel: { fontSize: 11, color: '#64748B', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: 8 },
  kpiValueError: { fontSize: 28, fontWeight: '900', color: '#DC2626' },
  kpiValueInfo: { fontSize: 28, fontWeight: '900', color: '#2563EB' },
  kpiSuffix: { fontSize: 14, color: '#64748B' },
  
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#0F172A' },
  seeAll: { fontSize: 14, color: '#16A34A', fontWeight: 'bold' },
  
  alertsList: { gap: 16 },
  alertCard: { backgroundColor: 'white', borderRadius: 12, padding: 16, borderWidth: 1, borderColor: '#E2E8F0', shadowColor: '#000', shadowOpacity: 0.03, shadowRadius: 4, elevation: 1 },
  alertTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  alertBadgeError: { backgroundColor: '#FEE2E2', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4, borderWidth: 1, borderColor: '#FCA5A5' },
  alertBadgeWarning: { backgroundColor: '#FFEDD5', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4, borderWidth: 1, borderColor: '#FDBA74' },
  alertBadgeText: { fontSize: 10, fontWeight: 'bold', color: '#0F172A' },
  alertConfidence: { fontSize: 12, fontWeight: 'bold', color: '#16A34A' },
  alertType: { fontSize: 18, fontWeight: 'bold', color: '#0F172A', marginBottom: 4 },
  alertZone: { fontSize: 14, color: '#64748B', marginBottom: 16 },
  actionButton: { backgroundColor: '#DC2626', padding: 12, borderRadius: 8, alignItems: 'center' },
  actionButtonText: { color: 'white', fontWeight: 'bold', fontSize: 14 },
  actionButtonSecondary: { backgroundColor: '#F1F5F9', padding: 12, borderRadius: 8, alignItems: 'center' },
  actionButtonTextSecondary: { color: '#0F172A', fontWeight: 'bold', fontSize: 14 },
});
