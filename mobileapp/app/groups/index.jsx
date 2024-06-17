import { View, StyleSheet, Text, FlatList } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import { useState } from "react";
import { router } from "expo-router";
import { dispatch, useSelector } from "react-redux";
import GroupChat from "components/groupchats";
import { SafeAreaView } from "react-native-safe-area-context";
import GoBackTopBar from "components/topBarGoBack";

export default function PostsPage() {
    const [refreshing, setRefreshing] = useState(false);
    const data = useSelector((state) => state.user.data);

    return (
        <SafeAreaView style={styles.mainContainer}>
            <GoBackTopBar title="Groups" />
            <FlatList
                style={styles.postsContainer}
                contentContainerStyle={styles.postsContentContainer}
                data={data.chats}
                renderItem={GroupChat}
                keyExtractor={(item) => item.id}
                onRefresh={() => console.log("hello")}
                refreshing={refreshing}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    mainContainer: {
        height: "100%",
        width: "100%",
    },
    postsContainer: {
        marginTop: 20,
        marginBottom: 20,
    },
    postsContentContainer: {
        rowGap: 20,
        paddingBottom: 50,
    },
});
