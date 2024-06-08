import { useEffect, useState, createContext, useContext } from 'react'
import { setItemAsync, getItemAsync } from 'expo-secure-store'
import { TokenResponse } from 'expo-auth-session';
import { jwtDecode } from 'jwt-decode'
import "core-js/stable/atob"; // Used to fix jwtDecode imports from core-js
import * as WebBrowser from 'expo-web-browser'
import * as AuthSession from 'expo-auth-session'
import { Alert } from 'react-native';

/* 

These functions allow you to securely store tokens in the device encrypted

setToken: stores the token
getCachedToken: gets the token
*/
const AUTH_STORAGE_KEY = "jwtToken";
const setToken = async (token) => setItemAsync(AUTH_STORAGE_KEY, token);
const getCachedToken = async () => getItemAsync(AUTH_STORAGE_KEY);


/* Settings for Auth0 */
const AUTH0_DOMAIN = "https://dev-ci0ohe1d547k4xmv.us.auth0.com";
const AUTH0_SETTINGS = {
    clientId: "oaGNeBKP9gAgI6CiyBuV9PTGc49kZZCH",
    domain: AUTH0_DOMAIN,
    authEndpoint: `${AUTH0_DOMAIN}/authorize`,
    tokenEndpoint: `${AUTH0_DOMAIN}/oauth/token`,
    redirectUri: AuthSession.makeRedirectUri({ scheme: "uwcourseconnect" }),
    scopes: ['openid', 'offline_access', 'read:groupchat', 'write:groupchat', 'read:profile', 'write:profile']
};

/* Let the web browser close correctly when using authenticating */
WebBrowser.maybeCompleteAuthSession();


/** Create a context wrapper for the login info */
const AuthContext = createContext(null);

export const useAuthContext = () => {
    // Function to get the context 

    const authProps = useContext(AuthContext);
    if (!authProps) Alert.alert('Object not wrapped in context');
    return authProps;
};

export const AuthContextProvider = ({ children }) => {
    // A wrapper provider for the values

    const [user, setUser] = useState({});

    /** Parameters for login */
    const [request, result, promptAsync] = AuthSession.useAuthRequest(
        {
            redirectUri: AUTH0_SETTINGS.redirectUri,
            clientId: AUTH0_SETTINGS.clientId,
            responseType: 'code',
            scopes: AUTH0_SETTINGS.scopes,
            extraParams: {
                audience: 'https://courseconnectapi.mattheway.com/',
                nonce: 'nonce'
            }
        },
        { authorizationEndpoint: AUTH0_SETTINGS.authEndpoint }
    );

    const logout = () => {
        /**
         * Used to clear the cache and all data pertaining to a user
         * Used in a logout button
         */
        setToken("");
        setUser({});
    };

    const readTokenFromStorage = async () => {

        // Retrieve Token
        const token = await getCachedToken();
        const tokenConfig = JSON.parse(token);

        if (!tokenConfig) return; // If there is nothing there

        let tokenResponse = new TokenResponse(tokenConfig); // Data on refresh token

        if (tokenResponse.shouldRefresh()) {
            const refreshConfig = { clientId: AUTH0_SETTINGS.clientId, refreshToken: tokenConfig.refreshToken };
            const endpointConfig = { tokenEndpoint: AUTH0_SETTINGS.tokenEndpoint };

            // Get a new token on refresh
            tokenResponse = await tokenResponse.refreshAsync(refreshConfig, endpointConfig);
            setToken(JSON.stringify(tokenResponse.getRequestConfig())); // Cache for later usage
        }

        const decoded = jwtDecode(tokenResponse.accessToken);
        setUser({ jwtToken: tokenResponse.accessToken, token: decoded }); // Update the current user
    };

    useEffect(() => {
        // Update contents whenever the result is changed
        readTokenFromStorage();
        if (!result) return;

        if (result.error) {
            Alert.alert('Authentication Error'), result.params.error_description || 'something went wrong';
            return;
        }

        if (result.type === 'success') {
            const code = result.params?.code;
            if (!code) return;

            // Retrieve access token and refresh token from code
            AuthSession.exchangeCodeAsync(
                {
                    code: code,
                    redirectUri: AUTH0_SETTINGS.redirectUri,
                    clientId: AUTH0_SETTINGS.clientId,
                    extraParams: {
                        code_verifier: request?.codeVerifier
                    }
                },
                { tokenEndpoint: AUTH0_SETTINGS.tokenEndpoint }
            ).then((res) => {
                const tokenConfig = res.getRequestConfig();
                const jwtToken = tokenConfig.accessToken;

                setToken(JSON.stringify(tokenConfig)); // Cache token
                setUser({jwtToken: jwtToken, token: jwtDecode(jwtToken)}); // Update user
            }).catch((err) => {
                console.log(err);
            });
        };

    }, [result]);

    return (
        <AuthContext.Provider value={{user: user, promptAsync: promptAsync, logout: logout}}>
            {children}
        </AuthContext.Provider>
    );
};

