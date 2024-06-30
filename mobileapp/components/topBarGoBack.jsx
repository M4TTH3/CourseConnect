import { router } from "expo-router";
import { StyleSheet, View, Text, StatusBar, TextInput } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";

/**
 * This provides the top bar with a router back navigation control
 * @param {title, cancel, confirm, confirmCallback} param0
 *
 * title: The title of the top bar
 * cancel: Whether to put an X for cancel instead of go back
 * confirm (str): Whether to put a text on topright with confirmCallback
 * confirmCallback: Callback function for the confirm button
 */
export default function GoBackTopBar({
    title,
    cancel,
    cancelCallback,
    confirm,
    confirmCallback,
}) {
    return (
        <View id="groupTopGrid" style={styles.topGrid}>
            {cancel ? (
                <Ionicons
                    name="close"
                    style={styles.topLeft}
                    size={30}
                    color="black"
                    onPress={() =>
                        cancelCallback ? cancelCallback() : router.back()
                    }
                />
            ) : (
                <Ionicons
                    name="chevron-back"
                    style={styles.topLeft}
                    size={30}
                    color="black"
                    onPress={() => router.back()}
                />
            )}
            <Text style={styles.title}>{title}</Text>
            {confirm ? (
                <Text style={styles.confirm} onPress={confirmCallback}>
                    Confirm
                </Text>
            ) : (
                <View style={{ width: 28, flex: 1 }}></View>
            )}

            <StatusBar
                backgroundColor="#FED34C"
                barStyle="dark-content"
                translucent={true}
            />
        </View>
    );
}

/**
 * Adds a search bar with a go back close. It allows for searchable
 *
 * @param {*} param0
 * @returns
 */
export function GoBackSearchTopBar({ cancel, cancelCallback, setInput, value }) {
    return (
        <View id="groupTopGrid" style={styles.topGrid}>
            {cancel ? (
                <Ionicons
                    name="close"
                    style={styles.topLeft}
                    size={30}
                    color="black"
                    onPress={() =>
                        cancelCallback ? cancelCallback() : router.back()
                    }
                />
            ) : (
                <Ionicons
                    name="chevron-back"
                    style={styles.topLeft}
                    size={30}
                    color="black"
                    onPress={() => router.back()}
                />
            )}
            <View style={styles.searchBar}>
                <TextInput
                    style={styles.searchBarInput}
                    inputMode="search"
                    enterKeyHint="search"
                    onChange={(e) => setInput(e.nativeEvent.text)}
                    value={value}
                ></TextInput>
                <MaterialCommunityIcons
                    name="magnify"
                    size={18}
                    style={styles.searchBarMagnify}
                />
            </View>
            <StatusBar
                backgroundColor="#FED34C"
                barStyle="dark-content"
                translucent={true}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    topGrid: {
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        width: "100%",
        height: 40,
        margin: "auto",
        paddingHorizontal: 15,
        paddingBottom: 10,
        backgroundColor: "#FED34C",
    },
    topLeft: {
        flex: 1,
        display: "flex",
        alignSelf: "flex-start",
        paddingTop: 2,
    },
    title: {
        fontSize: 24,
        fontWeight: "600",
        flex: 1,
        textAlign: "center",
        alignSelf: "center",
    },
    confirm: {
        fontSize: 18,
        fontWeight: "600",
        flex: 1,
        textAlign: "right",
        alignSelf: "flex-end",
    },
    searchBar: {
        flex: 6,
        fontSize: 18,
        backgroundColor: "white",
        borderColor: "black",
        borderWidth: 2,
        borderRadius: 5,
        alignSelf: "flex-start",
        paddingLeft: 5,
        paddingVertical: 5,
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "baseline",
        color: "black",
    },
    searchBarInput: {
        flex: 9,
    },
    searchBarMagnify: {
        flex: 1,
        marginRight: 0,
    },
});
