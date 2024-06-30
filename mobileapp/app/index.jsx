import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { useAuthContext } from "../components/customauth";

import {
    router,
    useRootNavigationState,
    Redirect,
    useFocusEffect,
} from "expo-router";
import { useCallback } from "react";

export default function App() {
    const { promptAsync, isLoggedIn } = useAuthContext();

    useFocusEffect(
      /**
       * Redirect to posts once we have logged in.
       * Docs: https://docs.expo.dev/router/reference/redirects/
       */
        useCallback(() => {
            if (isLoggedIn()) router.replace("/posts");
        }, [isLoggedIn])
    );

    return (
        <View style={styles.container}>
            <Text onPress={() => promptAsync()}>Index Page</Text>
            <StatusBar style="auto" />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        display: "flex",
        backgroundColor: "#fff",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
    },
});
