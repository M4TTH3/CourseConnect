import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';


/**
 * Will call the backend and update the current user given the access token.
 * 
 */
export const fetchUser = createAsyncThunk(
    'user/fetchUser', 
    async (accessToken, thunkAPI) => {
        
    },
);

/**
 * This will be used for testing purposes. 
 * 
 */
const initialUserData = {
    id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    blocked: [],
    reports: [],
    posts: [{
        course: "CSE 110",
        content_type: "Assignment",
        content_number: 1,
        size_limit: 0,
        course_code: "CSE110",
        description: "Assignment 1 for CSE 110",
        id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        post_date: 0,
        user_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        linked_chat: null,
    }],
    chats: [{
        id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        users: ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        size_limit: 4,
        course_code: "CSE110",
        course_name: "Introduction to Computer Science",
        content_type: "Assignment",
        content_number: 1,
        post_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    },
    {
        id: "3fa85f64-5717-4562-b3fc-2c963f66afa8",
        users: ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afa8"],
        size_limit: 4,
        course_code: "CSE110",
        course_name: "Data Structures and Algorithms",
        content_type: "Assignment",
        content_number: 3,
        post_id: "3fa85f64-5717-4562-b3fc-2c963f66afa8"
    },
    {
        id: "3fa85f64-5717-4562-b3fc-2c963f66afa9",
        users: ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afa9"],
        size_limit: 4,
        course_code: "CSE111",
        course_name: "Web Development",
        content_type: "Assignment",
        content_number: 4,
        post_id: "3fa85f64-5717-4562-b3fc-2c963f66afa9"
    },
    {
        id: "3fa85f64-5717-4562-b3fc-2c963f66afaa",
        users: ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afaa"],
        size_limit: 4,
        course_code: "CSE112",
        course_name: "Artificial Intelligence",
        content_type: "Assignment",
        content_number: 5,
        post_id: "3fa85f64-5717-4562-b3fc-2c963f66afaa"
    }]
}

/**
 * We want a state to store the data from a user.
 * 
 * user.data: {
 *     id: UUID,
 *     blocked: [ ],
 *     reports: [ ],
 *     posts: [ ],
 *     chats: [ ]
 * }
 * 
 * loading: bool - represents the current state in 
 * 
 */
const userSlice = createSlice({
    name: 'user',
    initialState: {
        data: initialUserData,
        loading: false,
        error: null,
    },
    extraReducers: (builder) => {
        builder.addCase(fetchUser.pending, (state) => {
            state.loading = true;
        })
        .addCase(fetchUser.fulfilled, (state, action) => {
            state.loading = false;
            state.data = action.payload;
        });
    }
});

export default userSlice.reducer;