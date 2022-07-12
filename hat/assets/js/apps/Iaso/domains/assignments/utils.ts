// types
import {
    AssignmentsApi,
    AssignmentApi,
    SaveAssignmentQuery,
} from './types/assigment';
import { OrgUnitMarker, OrgUnitShape, BaseLocation } from './types/locations';
import { Planning } from './types/planning';
import { DropdownTeamsOptions, SubTeam, User, Team } from './types/team';
import { OrgUnit } from '../orgUnits/types/orgUnit';

import { Profile, getDisplayName } from '../../utils/usersUtils';

export type AssignedUser = Profile & {
    color: string;
};

export type OrgUnitAssignedTeamUser = {
    assignment: AssignmentApi | undefined;
    assignedTeam: DropdownTeamsOptions | undefined;
    assignedUser: AssignedUser | undefined;
    emptyAssignment: AssignmentApi | undefined;
};

export const getOrgUnitAssignation = (
    assignments: AssignmentsApi,
    orgUnit: OrgUnitShape | OrgUnitMarker | BaseLocation | OrgUnit,
    teams: DropdownTeamsOptions[],
    profiles: Profile[],
    currentType: 'TEAM_OF_TEAMS' | 'TEAM_OF_USERS' | undefined,
): OrgUnitAssignedTeamUser => {
    let assignedTeam;
    let assignedUser;
    const assignment = assignments.find(
        ass => ass.org_unit === orgUnit.id && Boolean(ass.team || ass.user),
    );
    const emptyAssignment = assignments.find(
        ass => ass.org_unit === orgUnit.id && !ass.team && !ass.user,
    );
    if (assignment && (currentType === 'TEAM_OF_TEAMS' || !currentType)) {
        assignedTeam = teams.find(team => team.original.id === assignment.team);
    }
    if (assignment && (currentType === 'TEAM_OF_USERS' || !currentType)) {
        assignedUser = profiles.find(
            profile => profile.user_id === assignment.user,
        );
    }
    return {
        assignment,
        assignedTeam,
        assignedUser,
        emptyAssignment,
    };
};

type OrgunitParentProps = {
    currentTeam?: DropdownTeamsOptions;
    currentUser?: AssignedUser;
    teams?: DropdownTeamsOptions[];
    users?: Profile[];
};

export const getParentTeam = ({
    currentTeam,
    currentUser,
    teams,
}: OrgunitParentProps): DropdownTeamsOptions | undefined => {
    if (currentTeam && teams) {
        return teams.find(team =>
            team.original.sub_teams.includes(currentTeam.original.id),
        );
    }
    if (currentUser && teams) {
        return teams.find(team =>
            team.original.users.includes(currentUser.user_id),
        );
    }
    return undefined;
};

export const getTeamName = (
    selectedItem: SubTeam | User | undefined,
    currentTeam: Team | undefined,
    profiles: Profile[],
    teams: DropdownTeamsOptions[],
): string => {
    let fullItem;
    let displayString = '';
    if (selectedItem) {
        if (currentTeam?.type === 'TEAM_OF_USERS') {
            fullItem = profiles.find(
                profile => profile.user_id === selectedItem.id,
            );
            displayString = getDisplayName(fullItem);
        }
        if (currentTeam?.type === 'TEAM_OF_TEAMS') {
            fullItem = teams.find(team => team.original.id === selectedItem.id);
            displayString = fullItem.label;
        }
    }
    return displayString;
};

type SaveParamsProps = {
    allAssignments: AssignmentsApi;
    selectedOrgUnit: OrgUnitShape | OrgUnitMarker | BaseLocation | OrgUnit;
    teams: DropdownTeamsOptions[];
    profiles: Profile[];
    currentType: 'TEAM_OF_TEAMS' | 'TEAM_OF_USERS' | undefined;
    selectedItem: SubTeam | User;
    planning: Planning;
};

export const getSaveParams = ({
    allAssignments,
    selectedOrgUnit,
    teams,
    profiles,
    currentType,
    selectedItem,
    planning,
}: SaveParamsProps): SaveAssignmentQuery => {
    const { assignment, assignedTeam, assignedUser, emptyAssignment } =
        getOrgUnitAssignation(
            allAssignments,
            selectedOrgUnit,
            teams,
            profiles,
            currentType,
        );
    let saveParams: SaveAssignmentQuery = {
        planning: planning.id,
        org_unit: selectedOrgUnit.id,
    };

    // TODO: make it better, copy paste for now...
    if (currentType === 'TEAM_OF_TEAMS') {
        saveParams.team = selectedItem.id;
        let id = assignment?.id;
        if (!id && emptyAssignment) {
            id = emptyAssignment.id;
        }
        if (id) {
            if (assignedTeam) {
                if (selectedItem.id !== assignedTeam.original.id) {
                    // update assignment
                    saveParams = {
                        id,
                        ...saveParams,
                    };
                } else {
                    // fake delete assignment, remove team / user
                    saveParams = {
                        ...saveParams,
                        team: null,
                        user: null,
                        id,
                    };
                }
            } else {
                // update assignment after fake delete
                saveParams = {
                    id,
                    ...saveParams,
                };
            }
        }
    }
    if (currentType === 'TEAM_OF_USERS') {
        saveParams.user = selectedItem.id;
        let id = assignment?.id;
        if (!id && emptyAssignment) {
            id = emptyAssignment.id;
        }
        if (id) {
            if (assignedUser) {
                if (selectedItem.id !== assignedUser.user_id) {
                    // update assignment
                    saveParams = {
                        id,
                        ...saveParams,
                    };
                } else {
                    // fake delete assignment, remove team / user
                    saveParams = {
                        ...saveParams,
                        team: null,
                        user: null,
                        id,
                    };
                }
            } else {
                // update assignment after fake delete
                saveParams = {
                    id,
                    ...saveParams,
                };
            }
        }
    }
    return saveParams;
};

type MultiSaveParamsProps = {
    allAssignments: AssignmentsApi;
    selectedOrgUnits: Array<OrgUnitShape | OrgUnitMarker | BaseLocation>;
    teams: DropdownTeamsOptions[];
    profiles: Profile[];
    currentType: 'TEAM_OF_TEAMS' | 'TEAM_OF_USERS' | undefined;
    selectedItem: SubTeam | User;
    planning: Planning;
};

export const getMultiSaveParams = ({
    allAssignments,
    selectedOrgUnits,
    teams,
    profiles,
    currentType,
    selectedItem,
    planning,
}: MultiSaveParamsProps): SaveAssignmentQuery => {
    const orgUnitIds = selectedOrgUnits.map(orgUnit => orgUnit.id);
    const baseQuery = {
        planning: planning.id,
        org_units: orgUnitIds,
    };
    const currentAssignments = selectedOrgUnits.map(orgUnit => {
        const { assignment, assignedTeam, assignedUser, emptyAssignment } =
            getOrgUnitAssignation(
                allAssignments,
                orgUnit,
                teams,
                profiles,
                currentType,
            );
        return {
            id: orgUnit.id,
            assignment,
            assignedTeam,
            assignedUser,
            emptyAssignment,
        };
    });

    const orgUnitsToUpdate = currentAssignments
        .filter(
            assignment =>
                assignment?.assignedTeam?.original.id !== selectedItem.id,
        )
        .map(orgUnit => orgUnit.id);

    const allOrgUnitsAlreadySelected = orgUnitsToUpdate.length === 0;

    if (allOrgUnitsAlreadySelected) {
        return { ...baseQuery, team: null, user: null };
    }

    if (currentType === 'TEAM_OF_TEAMS') {
        return {
            ...baseQuery,
            org_units: orgUnitsToUpdate,
            team: selectedItem.id,
        };
    }
    if (currentType === 'TEAM_OF_USERS') {
        return {
            ...baseQuery,
            org_units: orgUnitsToUpdate,
            user: selectedItem.id,
        };
    }
    throw new Error(
        `expected currentType type to be TEAM_OF_TEAMS or TEAM_OF_USERS. Got ${currentType}`,
    );
};
