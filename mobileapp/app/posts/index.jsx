import {
    View,
    StyleSheet,
    TextInput,
    FlatList,
  } from "react-native";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import Feather from "@expo/vector-icons/Feather";
import AntDesign from '@expo/vector-icons/AntDesign';
import { randomUUID } from "expo-crypto";
import { useState } from "react";
import Post from "components/posts";
import { router } from "expo-router";

export default function PostsPage() {
  const [refreshing, setRefreshing] = useState(false);

  const DATA = [
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS241",
      course_name: "Introduction to Sequential Programming Introduction to Sequential Programming",
      content_type: "Assignment",
      size_limit: 2,
      content_number: 5,
      linked_chat: {
        users: [randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID(), randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID(), randomUUID(), randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID()],
      },
    },
    {
      id: randomUUID(),
      post_date: new Date().valueOf(),
      user_id: randomUUID(),
      course: "CS341",
      course_name: "Algorithms",
      content_type: "Quiz",
      content_number: 2,
      size_limit: 4,
      linked_chat: {
        users: [randomUUID()],
      },
    },
  ];

  return (
    <View style={styles.mainContainer}>
      <View id="postTopGrid" style={styles.postTopGrid}>
        <MaterialIcons name="menu" size={30} style={styles.topGridButton} />
        <View id="postRefineSearch" style={styles.postRefineSearch}>
          <TextInput
            style={styles.searchInput}
            placeholderTextColor="black"
            placeholder="Search Groups..."
          />
          <MaterialCommunityIcons
            name="magnify"
            id="search-icon"
            color={"black"}
            size={25}
            style={styles.searchIcon}
            onPress={(e) => e}
          />
        </View>
        <Feather
          name="plus"
          onPress={(e) => e}
          size={32}
          style={styles.topGridButton}
        />
        <AntDesign
          name="message1"
          size={24}
          style={styles.topGridButton}
          onPress={() => router.push('/groups')}
        />
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
  postTopGrid: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    width: "100%",
    height: 40,
    margin: "auto",
    paddingHorizontal: 10
  },
  postRefineSearch: {
    display: "flex",
    flexDirection: "row",
    width: "60%",
    alignItems: "center",
    backgroundColor: "#DFDFDF",
    borderRadius: 20,
    height: 34,
  },
  searchInput: {
    flex: 5,
    paddingLeft: 10,
    fontWeight: "500",
  },
  searchIcon: {
    flex: 1,
  },
  topGridButton: {
    textAlign: "center",
    backgroundColor: "transparent",
    color: "black",
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