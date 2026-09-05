import { Tabs } from 'expo-router';
import { View, Text } from 'react-native';

export default function Layout() {
  return (
    <Tabs screenOptions={{
        headerShown: true,
        headerStyle: { backgroundColor: '#052E16' },
        headerTintColor: '#fff',
        tabBarStyle: { backgroundColor: '#ffffff', borderTopWidth: 1, borderTopColor: '#e2e8f0', height: 60, paddingBottom: 8, paddingTop: 8 },
        tabBarActiveTintColor: '#16A34A',
        tabBarInactiveTintColor: '#64748B',
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Accueil',
          headerTitle: 'GeoGuard Executive',
          tabBarIcon: ({ color }) => (
            <View style={{ width: 24, height: 24, backgroundColor: color, borderRadius: 4 }} />
          ),
        }}
      />
      <Tabs.Screen
        name="carte"
        options={{
          title: 'Carte',
          headerTitle: 'Situation Territoriale',
          tabBarIcon: ({ color }) => (
            <View style={{ width: 24, height: 24, backgroundColor: color, borderRadius: 12 }} />
          ),
        }}
      />
      <Tabs.Screen
        name="alertes"
        options={{
          title: 'Alertes',
          headerTitle: 'Alertes Prioritaires',
          tabBarIcon: ({ color }) => (
            <View style={{ width: 24, height: 24, borderColor: color, borderWidth: 2, borderRadius: 4 }} />
          ),
        }}
      />
      <Tabs.Screen
        name="analyses"
        options={{
          title: 'Analyses',
          headerTitle: 'Analyses & Rapports',
          tabBarIcon: ({ color }) => (
            <View style={{ width: 24, height: 12, backgroundColor: color, borderRadius: 2 }} />
          ),
        }}
      />
    </Tabs>
  );
}
