import { SafeAreaView } from "react-native-safe-area-context";
import GoBackTopBar, { GoBackSearchTopBar } from "components/topBarGoBack";
import {
    View,
    StyleSheet,
    TextInput,
    Text,
    Pressable,
    Modal,
    FlatList,
} from "react-native";
import { useEffect, useState } from "react";
import MaterialCommunityIcons from "@expo/vector-icons/MaterialCommunityIcons";
import { BlurView } from "expo-blur";
import { Dropdown } from "react-native-element-dropdown";
import useBackendApi from "components/dataApi";

const dropdownOptions = [
    {
        label: "Assignment",
        value: "assignment",
    },
    {
        label: "Quiz",
        value: "quiz",
    },
    {
        label: "Lab",
        value: "lab",
    },
    {
        label: "Midterm",
        value: "midterm",
    },
    {
        label: "Final",
        value: "final",
    },
];

export default function CreatePost() {
    const [inputs, setInputs] = useState({});
    const [modalVisible, setModalVisible] = useState(false);
    const [modalSearch, setModalSearch] = useState(""); // Modal Search Input
    const [modalData, setModalData] = useState([]);

    const { callApi, isLoading } = useBackendApi();

    /**
     * This function will make an API call to create a post.
     */
    useEffect(() => {

        // Make a controller to cancel calls when we edit search
        const controller = new AbortController();
        const signal = controller.signal;

        // Make an API call to get the courses
        const uri = "posts/courses";
        callApi({
            uri: uri,
            queryParams: { filter: modalSearch },
            method: "GET",
            signal: signal,
        })
            .then((data) => {
                setModalData(data?.courses);
            })
            .catch((err) => {
                console.error(err);
            });

        return () => {
            console.log("Aborting fetch for modalSearch", modalSearch);
            controller.abort();
        };
    }, [modalSearch]);

    return (
        <SafeAreaView>
            <Modal
                visible={modalVisible}
                animationType="slide"
                onRequestClose={() => setModalVisible(false)}
            >
                <GoBackSearchTopBar
                    title=""
                    cancel
                    cancelCallback={() => setModalVisible(false)}
                    setInput={setModalSearch}
                    value={modalSearch}
                />
                <FlatList
                    data={modalData}
                    renderItem={({ item }) => (
                        <CourseSelection
                            {...item}
                            setInputs={setInputs}
                            closeWindow={() => setModalVisible(false)}
                        />
                    )}
                    refreshing={isLoading}
                    onRefresh={() => {}}
                />
            </Modal>

            <GoBackTopBar title="Create Post" cancel confirm="Confirm" />
            <View style={[styles.container]}>
                <View style={styles.topContainer}>
                    <View style={styles.postBlurWrapper}>
                        <BlurView
                            intensity={40}
                            tint="systemThickMaterialLight"
                            experimentalBlurMethod="dimezisBlurView"
                        >
                            <Pressable
                                style={styles.postItem}
                                onPress={() => setModalVisible(true)}
                            >
                                <Text style={styles.postItemText}>
                                    {inputs.course_code ?? "Course Code"}
                                </Text>
                                <MaterialCommunityIcons
                                    name="magnify"
                                    size={24}
                                />
                            </Pressable>
                        </BlurView>
                    </View>

                    <View style={[styles.courseInfo]}>
                        <Text style={[styles.courseInfoBold]}>
                            Course Name:{" "}
                            <Text style={{ fontWeight: "normal" }}>
                                {inputs?.course_name ?? ""}
                            </Text>
                        </Text>
                        <View>
                            <Text style={[styles.courseInfoBold]}>
                                Description:
                            </Text>
                            <Text numberOfLines={4}>
                                {inputs?.description ?? ""}
                            </Text>
                        </View>
                    </View>
                </View>

                <View style={styles.bottomContainer}>
                    <View style={styles.postBlurWrapper}>
                        <Dropdown
                            style={styles.postItem}
                            data={dropdownOptions}
                            labelField="label"
                            valueField="value"
                            placeholder="Content Type..."
                            onChange={(item) =>
                                setInputs((prev) => ({
                                    ...prev,
                                    content_type: item.value,
                                }))
                            }
                        ></Dropdown>
                    </View>

                    <View style={styles.postBlurWrapper}>
                        <View style={styles.postItem}>
                            <TextInput
                                style={styles.postItemText}
                                placeholder="Content Number..."
                                keyboardType="number-pad"
                                onChange={(e) =>
                                    setInputs((prev) => ({
                                        ...prev,
                                        content_number: e.nativeEvent?.text,
                                    }))
                                }
                            />
                        </View>
                    </View>

                    <View style={styles.postBlurWrapper}>
                        <View style={styles.postItem}>
                            <TextInput
                                style={[
                                    styles.postItemText,
                                    styles.description,
                                ]}
                                placeholder="Description..."
                                multiline
                                numberOfLines={8}
                            />
                        </View>
                    </View>
                </View>
            </View>
        </SafeAreaView>
    );
}

/**
 * Returns a JSX item to select one of the courses.
 *
 * @param {*} props
 */
const CourseSelection = ({
    course_code,
    course_name,
    description,
    setInputs,
    closeWindow
}) => {
    const handlePress = () => {
        setInputs((prev) => {
            closeWindow();

            return {
                ...prev,
                course_code: course_code,
                course_name: course_name,
                description: description,
            };
        });
    };

    return (
        <Pressable onPress={handlePress}>
            <View style={modalStyles.container}>
                <Text style={modalStyles.code} numberOfLines={1}>
                    {course_code}
                </Text>
                <Text style={modalStyles.name} numberOfLines={1}>
                    {course_name}
                </Text>
                <Text style={modalStyles.description} numberOfLines={4}>
                    {description}
                </Text>
            </View>
        </Pressable>
    );
};

const modalStyles = StyleSheet.create({
    container: {
        padding: 10,
        paddingBottom: 20,
        borderColor: "black",
        borderBottomWidth: 2,
        height: 150,
        backgroundColor: "white",
        overflow: "hidden",
    },
    code: {
        fontSize: 24,
        fontWeight: "600",
    },
    name: {
        fontSize: 18,
    },
    description: {
        fontSize: 12,
    },
});

const styles = StyleSheet.create({
    container: {
        display: "flex",
        flexDirection: "column",
        paddingVertical: 30,
        paddingHorizontal: 10,
        height: "100%",
        width: "100%",
    },
    postBlurWrapper: {
        overflow: "hidden",
        borderRadius: 10,
    },
    postItem: {
        width: "100%",
        borderColor: "black",
        borderWidth: 2,
        borderRadius: 10,
        padding: 10,
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    postItemText: {
        fontSize: 18,
    },
    description: {
        verticalAlign: "top",
    },
    bottomContainer: {
        flex: 3,
        display: "flex",
        flexDirection: "column",
        width: "100%",
        gap: 25,
    },
    topContainer: {
        flex: 1,
        display: "flex",
        flexDirection: "column",
        width: "100%",
        gap: 25,
    },
    courseInfo: {
        paddingHorizontal: 10,
    },
    courseInfoBold: {
        fontWeight: "bold",
    },
});
