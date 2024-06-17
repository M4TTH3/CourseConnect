import { router } from "expo-router";
import { View, Text, Pressable, StyleSheet } from "react-native";

export default function GroupChat({ item: groupchat }) {
    const enterChat = () => {
        /**
         * Enters the chat w.r.t to the specific ID and the course_code.
         * Injects the necessary info for the group chat.
         */
        router.push(`/groups/chats/${groupchat.id}?course_code=${groupchat.course_code}`);
    };

    return (
        <Pressable style={chatStyles.chatContainer} onPress={enterChat}>
            <Text style={chatStyles.courseCode}>{groupchat?.course_code}</Text>
            <Text numberOfLines={1} style={chatStyles.courseName}>
                {groupchat?.course_name}
            </Text>
            <View style={chatStyles.bottomBar}>
                <Text style={chatStyles.memberCount}>
                    {groupchat?.users.length} Members
                </Text>
            </View>
        </Pressable>
    );
}

const chatStyles = StyleSheet.create({
    chatContainer: {
        height: 140,
        width: "85%",
        paddingTop: 15,
        paddingBottom: 5,
        paddingLeft: 20,
        paddingRight: 20,
        borderColor: "#E0E0E0",
        borderWidth: 2,
        borderRadius: 10,
        color: "black",
        alignSelf: "center",
    },
    courseCode: {
        fontSize: 40,
        fontWeight: "500",
    },
    courseName: {
        width: "70%",
        fontWeight: "500",
        fontSize: 15,
        overflow: "hidden",
    },
    bottomBar: {
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        marginTop: 10,
    },
    memberCount: {
        color: "#919191",
        marginTop: 5,
    },
    joinButton: {
        width: "20%",
        height: "20%",
        backgroundColor: "#FED34C",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 20,
    },
});
