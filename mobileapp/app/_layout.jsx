import { Slot } from 'expo-router';
import { AuthContextProvider } from 'components/customauth';
import { SafeAreaView } from 'react-native-safe-area-context';

export default Layout = () => {
    return (
        <AuthContextProvider>
            <SafeAreaView>
                <Slot />
            </SafeAreaView>
        </AuthContextProvider>
    )
}