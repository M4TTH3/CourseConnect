import { useLocalSearchParams } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import { GiftedChat, Send } from "react-native-gifted-chat";
import GoBackTopBar from "components/topBarGoBack";
import { SafeAreaView } from "react-native-safe-area-context";
import Ioniocons from "@expo/vector-icons/Ionicons";

/**
 * This file is responsible for rendering the chat screen for a group.
 *
 * Opens a websocket connection to the backend to connect into the chat room.
 *
 * Credit:
 * - Chat Interface: https://github.com/FaridSafi/react-native-gifted-chat (react-native-gifted-chat by Farid Safi)
 *
 */

export default function GroupChat() {
    const { id, course_code } = useLocalSearchParams();
    console.log(course_code);
    console.log(id);

    const [messages, setMessages] = useState([]);

    useEffect(() => {
        setMessages([
            {
                _id: 1,
                text: "Hello developer",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 2,
                text: "How are you?",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 3,
                text: "I'm doing great!",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 4,
                text: "What about you?",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 5,
                text: "I'm also doing well, thanks!",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 6,
                text: "That's good to hear!",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 7,
                text: "What have you been working on lately?",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 8,
                text: "I've been working on a new feature for our app.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 9,
                text: "That sounds exciting! Tell me more about it.",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 10,
                text: "Sure! We're adding a chat feature to our app.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 11,
                text: "That's awesome! Chat functionality is always useful.",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 12,
                text: "Yes, it will make communication between users much easier.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 13,
                text: "I'm glad to hear that. How is the implementation going?",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 14,
                text: "It's going well. We're using the GiftedChat library for the UI.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 15,
                text: "That's a great choice. GiftedChat is very popular and easy to use.",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 16,
                text: "Yes, it has all the features we need for our chat functionality.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 17,
                text: "I'm looking forward to seeing the final result.",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 18,
                text: "Thank you! I'll make sure to keep you updated on our progress.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
            {
                _id: 19,
                text: "That would be great. Good luck with the implementation!",
                createdAt: new Date(),
                user: {
                    _id: 2,
                    name: "React Native",
                },
            },
            {
                _id: 20,
                text: "Thank you! I appreciate your support.",
                createdAt: new Date(),
                user: {
                    _id: 1,
                    name: "React Native",
                },
            },
        ]);
    }, []);

    const onSend = useCallback((messages = []) => {
        setMessages((previousMessages) =>
            GiftedChat.append(previousMessages, messages)
        );
    }, []);

    return (
        <SafeAreaView style={styles.ChatContainer}>
            <GoBackTopBar title="Chat" />
            <GiftedChat
                messages={messages}
                onSend={(messages) => onSend(messages)}
                user={{
                    _id: 1,
                }}
                alwaysShowSend
                renderAvatar={null}
                renderUsernameOnMessage
                renderSend={renderSend}
                loadEarlier
                onLoadEarlier={() => console.log('loading earlier')}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    ChatContainer: {
        height: "100%",
        width: "100%",
    },
    SendButton: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
});

const renderSend = (props) => {
    /**
     * Custon send icon for the messages
     */

    return (
        <Send {...props} >
            <View
                style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginRight: 10,
                    marginBottom: 8,
                }}
            >
                <Ioniocons
                    style={styles.SendButton}
                    name="send"
                    size={24}
                    color="#2B68E6"
                />
            </View>
        </Send>
    );
};
