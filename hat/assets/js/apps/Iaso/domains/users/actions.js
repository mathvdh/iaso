import { saveAction } from '../../redux/actions/formsActions';

export const SET_CURRENT_USER = 'SET_CURRENT_USER';

export const setCurrentUser = payload => ({
    type: SET_CURRENT_USER,
    payload,
});

const apiKey = 'profiles';

export const saveCurrentUserProFile = profile => dispatch =>
    saveAction(
        dispatch,
        { ...profile, id: 'me' },
        apiKey,
        'saveUserSuccessful',
        'saveUserError',
        null,
        undefined,
        setCurrentUser,
    );
