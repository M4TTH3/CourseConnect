import { View, StyleSheet, TextInput, FlatList } from "react-native"
import MaterialIcons from "@expo/vector-icons/MaterialIcons"
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons"
import Feather from "@expo/vector-icons/Feather"
import { Image } from "expo-image"

export default function Posts() {

    return (
        <View>
            <View id="postTopGrid" >
                <MaterialIcons name="menu" size={32}/>
                <View id="postRefineSearch">
                    <TextInput placeholder="Search Groups..." />
                    <MaterialCommunityIcons.Button name="magnify" onPress={e => e} size={32} />
                </View>
                <Feather name="plus" onPress={e => e}/>
                <Image />
            </View>
            <FlatList />
        </View>
    );
}