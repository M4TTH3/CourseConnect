import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { useAuthContext } from '../components/customauth';
import { router } from 'expo-router';
import { useEffect } from 'react';

export default function App() {
  const { user, promptAsync } = useAuthContext();

  return (
    <View style={styles.container}>
      <Text onPress={() => router.replace('posts')}>Index Page</Text>
      <StatusBar style="auto" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    display: "flex",
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    width: "100%",
    height: "100%",
  },
});
