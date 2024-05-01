import { Slot } from 'expo-router';
import { AuthContextProvider } from '../components/customauth';

export default Layout = () => {
    return (
        <AuthContextProvider>
            <Slot />
        </AuthContextProvider>
    )
}