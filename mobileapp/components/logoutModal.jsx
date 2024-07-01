import React from 'react';
import { Modal, View, Text, Button, StyleSheet, Pressable } from 'react-native';
import { useAuthContext } from './customauth';
import { BlurView } from 'expo-blur';
import MaterialIcons from "@expo/vector-icons/MaterialIcons";

const LogoutModal = ({ modalVisible, disableModal }) => {

    const { logout } = useAuthContext();

    const handleCancel = () => {
        // Disable the Modal
        disableModal();
    }

    const handleLogout = () => {
        // Add your logout logic here
        // e.g. clear user session, navigate to login screen, etc.
        logout();
    };

    return (
        <View>
            <Modal
                animationType='fade'
                transparent={true}
                visible={modalVisible}
                onRequestClose={() => handleCancel()}
            >
                <BlurView intensity={50} tint='systemChromeMaterialDark' style={styles.innerModalContainer} experimentalBlurMethod='dimezisBlurView' >
                    <View style={styles.optionsContainer}>
                        <MaterialIcons name="logout" style={{alignSelf: 'center'}} size={40} color="black"/>
                        <Text>Logout from Course Connect?</Text>
                        <Pressable onPress={handleCancel} style={styles.cancelButton}>
                            <Text style={styles.cancelText}>Cancel</Text>
                        </Pressable>
                        <Pressable onPress={handleLogout} style={styles.logoutButton}>
                            <Text style={styles.logoutText}>Logout</Text>
                        </Pressable>
                    </View>
                </BlurView>
            </Modal>
        </View>
    );
};

const styles = StyleSheet.create({
    innerModalContainer: { 
        width: "100%",
        height: "100%", 
        justifyContent: 'center', 
        alignItems: 'center'
    },
    optionsContainer: {
        paddingHorizontal: 40,
        paddingVertical: 10,
        width: "70%",
        height: "30%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        rowGap: 10,
        backgroundColor: "white",
        borderRadius: 20,
    },
    logoutButton: {
        borderRadius: 30,
        textAlign: "center",
        backgroundColor: "#FED34C",
        width: "100%",
        height: "15%",
        display: "flex",
        justifyContent: "center",
    },
    logoutText: {
        textAlign: "center",    
        fontSize: 18,
        fontWeight: "600",
    },
    cancelButton: {
        borderRadius: 30,
        textAlign: "center",
        backgroundColor: "#000000",
        width: "100%",
        height: "15%",
        display: "flex",
        justifyContent: "center",
    },
    cancelText: {
        textAlign: "center",
        color: "white",    
        fontSize: 18,
        fontWeight: "600",
    }

});

export default LogoutModal;