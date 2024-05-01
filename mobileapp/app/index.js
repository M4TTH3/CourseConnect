import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { useAuthContext } from '../components/customauth';


export default function App() {
  const { user, promptAsync } = useAuthContext();

  return (
    <View style={styles.container}>
      <Text onPress={() => promptAsync()}>Index Page</Text>
      <StatusBar style="auto" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
