import { View, Text, StyleSheet } from 'react-native';

export default function Analyses() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Module Analyses en cours de développement...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F8FAFC' },
  text: { fontSize: 16, color: '#64748B', fontWeight: 'bold' }
});
