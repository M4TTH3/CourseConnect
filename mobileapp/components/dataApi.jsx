import { useCallback, useState, useEffect } from "react";
import { useAuthContext } from "components/customauth";
import Constants from "expo-constants";

/**
 * This file will allow for calling the API and storing api call states.
 *
 */
export default function useBackendApi() {
    // We will use a stack to determine how many API calls are being made.
    // If the stack is empty, then we can hide the loading spinner.
    const [isLoading, setIsLoading] = useState(false); 
    const [loadingStack, setLoadingStack] = useState(0);
    const [error, setError] = useState(null);

    const { getToken } = useAuthContext();

    // Get the base URL from either local or production.
    const { expoConfig } = Constants;
    const baseUrl = expoConfig?.hostUri ? "http://10.0.2.2:8000": process.env.EXPO_PUBLIC_API_URL;

    useEffect(() => {
        // Update the isLoading depending on loadingStack changes.
        setIsLoading(loadingStack > 0);

    }, [loadingStack]);

    /**
     *
     * @param { uri: String, queryParams: Object, method: String, body: Object } param0
     * @returns Promise
     */
    const callApi = async ({ uri, queryParams, method, body, signal }) => {
        setLoadingStack((prev) => prev + 1);

        // set the endpoint with the query params
        const endpoint = new URL(uri, baseUrl);
        Object.keys(queryParams).forEach((key) => 
            endpoint.searchParams.append(key, queryParams[key]));

        // Make a call to the API
        const token = await getToken();
        try {
            const response = await fetch(endpoint, {
                method: method,
                body: body ? JSON.stringify(body) : null,
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                signal: signal
            });
    
            // Check for the errors
            if (!response.ok) {
                setError(response.statusText);
                setLoadingStack((prev) => prev - 1);
                return null;
            }
    
            setLoadingStack((prev) => prev - 1);
            return await response.json();
        } catch (err) {
            setError(err);
            setLoadingStack((prev) => prev - 1);
            return null;
        }
    };

    return { callApi: useCallback(callApi, []), isLoading: isLoading, error: error }
}
