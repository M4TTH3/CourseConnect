import {
    View,
    StyleSheet,
    Text,
    FlatList,
  } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import { randomUUID } from "expo-crypto";
import { useState } from "react";
import Post from "components/posts";
import { router } from "expo-router";

export default function PostsPage() {
  const [refreshing, setRefreshing] = useState(false);

  const DATA = [

  ];

  return (
    <View style={styles.mainContainer}>
      <View id="groupTopGrid" style={styles.groupTopGrid}>
        <Ionicons name="chevron-back" size={28} color="black" onPress={() => router.back()}/>
        <Text style={styles.topGridName}>Groups</Text>
      </View>
      <FlatList
        style={styles.postsContainer}
        contentContainerStyle={styles.postsContentContainer}
        data={DATA}
        renderItem={Post}
        keyExtractor={(item) => item.id}
        onRefresh={() => console.log('hello')}
        refreshing={refreshing}
      />


    </View>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    height: "100%",
    width: "100%",
  },
  groupTopGrid: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "flex-start",
    alignItems: "center",
    gap: 20,
    width: "100%",
    height: 40,
    margin: "auto",
    paddingHorizontal: 10
  },
  topGridName: {
    fontSize: 18,
    fontWeight: "600",
  },
  postsContainer: {
    marginTop: 20,
    marginBottom: 20,
  },  
  postsContentContainer: {
    rowGap: 20, 
    paddingBottom: 50,
  }
});