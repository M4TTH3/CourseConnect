import { Slot } from 'expo-router';
import { AuthContextProvider } from 'components/customauth';
import { configureStore } from '@reduxjs/toolkit';
import { Provider } from "react-redux";
import userReducer from "slices/userSlice";
import { StyleSheet, View, StatusBar } from 'react-native';

const store = configureStore({
    reducer: {
        user: userReducer
    },

});

export default Layout = () => {
    /**
     * Redirect to home page if not logged in
     */

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