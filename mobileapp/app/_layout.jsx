import { Slot } from 'expo-router';
import { AuthContextProvider } from 'components/customauth';
import { configureStore } from '@reduxjs/toolkit';
import { Provider } from "react-redux";
import userReducer from "slices/userSlice";
import { View } from 'react-native';

const store = configureStore({
    reducer: {
        user: userReducer
    },

});

export default Layout = () => {
    
    return (
        <Provider store={store}>
            <AuthContextProvider>
                <View>
                    <Slot />
                </View>
            </AuthContextProvider>
        </Provider>   
    )
}