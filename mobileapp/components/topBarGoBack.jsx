import { router } from "expo-router";
import { StyleSheet, View, Text } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons"

/**
 * This provides the top bar with a router back navigation control
 * @param {title} param0
 */
export default function GoBackTopBar({ title }) {

    return (
        <View id="groupTopGrid" style={styles.topGrid}>
            <Ionicons
                name="chevron-back"
                size={28}
                color="black"
                onPress={() => router.back()}
            />
            <Text style={styles.topGridName}>{title}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    topGrid: {
        display: "flex",
        flexDirection: "row",
        justifyContent: "flex-start",
        alignItems: "center",
        gap: 20,
        width: "100%",
        height: 40,
        margin: "auto",
        paddingHorizontal: 10,
    },
    topGridName: {
        fontSize: 18,
        fontWeight: "600",
    },
});