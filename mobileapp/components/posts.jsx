import { View, Text, Pressable, StyleSheet } from "react-native";

export default function Post ({ item: postData }) {
    return (
      <View style={postStyles.postContainer}>
        <Text style={postStyles.courseCode}>{postData?.course_code}</Text>
        <Text numberOfLines={1} style={postStyles.courseName}>{postData?.course_name}</Text>
        <View style={postStyles.bottomBar}>
          <Text style={postStyles.memberCount}>{postData?.linked_chat.users.length}/{postData?.size_limit} Members</Text>
          <Pressable style={postStyles.joinButton}>
            <Text>Join</Text>
          </Pressable>
        </View>
      </View>
    );
  };
  
  const postStyles = StyleSheet.create({
    postContainer: {
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
      fontWeight: "500"
    },
    courseName: {
      width: "70%",
      fontWeight: "500",
      fontSize: 15,
      overflow: "hidden"
    },
    bottomBar: {
      width: "100%",
      height: "100%",
      display: "flex",
      flexDirection: "row",
      justifyContent: "space-between",
      marginTop: 10
    },
    memberCount: {
      color: "#919191",
      marginTop: 5
    },
    joinButton: {
      width: "20%",
      height: "20%",
      backgroundColor: "#FED34C",
      alignItems: "center",
      justifyContent: "center",
      borderRadius: 20
    },
  });