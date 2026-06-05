> Responsible Disclosure Research by Enis Aksu
> 
> This research is published to help defenders, security teams, and incident responders understand a potential limitation of Microsoft Teams session revocation when remote control sessions are already active.
> 
> No exploit code is provided. The goal of this publication is to improve defensive awareness and encourage organizations to evaluate their Teams remote control policies.

---

## 🎥 Proof of Concept

[![Watch the PoC Video](https://img.youtube.com/vi/0T12F7WIBQM/maxresdefault.jpg)](https://www.youtube.com/watch?v=0T12F7WIBQM)

---



## Executive Summary

During security testing of Microsoft Teams remote control functionality, I identified a behavior where an active remote control session remains operational after the controlling user's Microsoft Entra ID sessions have been revoked.

Microsoft reviewed the finding through the Microsoft Security Response Center (MSRC) and determined that the behavior does not meet the bar for a security vulnerability.

From an enterprise incident response perspective, however, the behavior may create a gap between expected containment and actual containment.

Organizations commonly revoke sessions as one of the first actions taken after detecting a compromised account. In my testing, session revocation successfully prevented the attacker from establishing new Teams interactions, but it did not terminate an already-established remote control session.

As a result, a user whose authentication session had been revoked could continue interacting with a victim workstation through an active Teams remote control session.

---

# Background

Microsoft Teams allows participants to request and receive control of another participant's shared desktop or application window.

Once approved, the remote participant can interact with the remote operating system using keyboard and mouse input.

This functionality is commonly used by:

- IT support teams
    
- Helpdesk personnel
    
- Trainers
    
- Consultants
    
- Internal support engineers
    

Because the feature grants direct interaction with a remote workstation, many organizations rely on authentication controls and session management to ensure access remains authorized.

---

# Test Environment

## Components

- Microsoft Teams Desktop Client
    
- Windows Workstations
    
- Microsoft Entra ID
    
- Two test accounts
    

### Account A

Controller / Attacker

### Account B

Victim

---

# Reproduction Steps

1. Account A joins a Teams meeting.
    
2. Account B joins the same meeting.
    
3. Account B shares their desktop.
    
4. Account A requests remote control.
    
5. Account B approves the request.
    
6. Remote control is verified.
    
7. Session revocation is executed against Account A.
    
8. Revocation is confirmed in Microsoft Entra audit logs.
    
9. Teams prompts Account A to sign in again.
    
10. Without re-authenticating, Account A continues interacting with the victim system.
    

---

# Observed Behavior

## Correctly Blocked

Following revocation:

- New screen sharing sessions are blocked.
    
- New remote control requests are blocked.
    
- Additional authenticated Teams actions are blocked.
    

This demonstrates that authentication enforcement occurs correctly for new interactions.

## Unexpectedly Allowed

The already-established remote control session remains active.

The revoked user can continue:

- Moving the mouse
    
- Typing keyboard input
    
- Opening applications
    
- Interacting with the operating system
    
- Performing administrative actions if permitted on the target system
    

---

# Demonstration

After session revocation was confirmed:

- Command Prompt was launched.
    
- A local user account was created.
    
- The user was added to the local Administrators group.
    
- Additional operating system interaction remained possible.
    

At the same time, Teams displayed a sign-in requirement, confirming that the user's authentication session had already been revoked.

---

# Technical Analysis

The observed behavior appears consistent with a separation between two different communication planes.

## Signaling Plane

Responsible for:

- Authentication
    
- Meeting management
    
- Session establishment
    
- Remote control negotiation
    

This component correctly honors session revocation.

## Media / Remote Control Plane

Responsible for:

- Audio
    
- Video
    
- Screen sharing
    
- Keyboard and mouse transport
    

Once established, this channel appears to continue operating independently of subsequent authentication state changes.

The result is a partial enforcement model:

|Action|Result After Revocation|
|---|---|
|New Screen Share|Blocked|
|New Remote Control Request|Blocked|
|Chat Activity|Blocked|
|Existing Remote Control Session|Continues|
|Existing Audio/Video Session|Continues|

---

# Security Implications

This research does **not** demonstrate an authentication bypass.

The attacker must still:

1. Possess a valid Teams account.
    
2. Join a meeting.
    
3. Request control.
    
4. Receive explicit approval from the victim.
    

However, once those conditions are met, session revocation alone may not fully contain the threat.

This creates a potential incident response gap where defenders believe access has been removed while an already-established remote control session remains operational.

---

# Example Attack Scenario

1. An attacker compromises a Teams account.
    
2. The attacker impersonates IT support.
    
3. A user shares their screen.
    
4. The user approves a remote control request.
    
5. Security monitoring detects suspicious activity.
    
6. The SOC revokes the attacker's sessions.
    
7. Incident responders believe containment has been achieved.
    
8. The attacker continues interacting with the victim workstation through the active remote control session.
    

The organization believes access has been removed while interactive control still exists.

---

# Workaround

Organizations that do not require Microsoft Teams remote control functionality should consider disabling the feature through Teams Meeting Policies.

Microsoft provides a policy setting named:

**Participants can give or request control**

When disabled, users can no longer:

- Give control
    
- Receive control
    
- Request control
    

during Teams meetings.

## Teams Admin Center

1. Open Teams Admin Center.
    
2. Navigate to:
    
    Meetings → Meeting Policies
    
3. Edit the policy assigned to users.
    
4. Under **Content Sharing**, locate:
    
    **Participants can give or request control**
    
5. Set the option to:
    
    **Off**
    
6. Save the policy.
    

## PowerShell

```powershell
Set-CsTeamsMeetingPolicy `
    -Identity Global `
    -AllowParticipantGiveRequestControl $False
```

## Additional Hardening Recommendations

Organizations should also consider:

- Restricting who can present during meetings.
    
- Using "Only organizers and co-organizers" as the default presenter role.
    
- Limiting screen-sharing permissions.
    
- Reviewing guest and external participant permissions.
    
- Including active Teams meeting termination within incident response playbooks.
    

## Operational Considerations

Disabling remote control may impact:

- Helpdesk support
    
- Remote troubleshooting
    
- Training sessions
    
- Collaborative support workflows
    

Organizations should evaluate the operational impact before deployment.

---

# Vendor Response

The finding was reported responsibly to Microsoft through MSRC.

Microsoft reviewed the report and determined that the behavior does not meet the criteria for a security vulnerability requiring servicing.

This publication is intended to document the behavior so that security teams can evaluate whether their incident response procedures adequately address active Teams remote control sessions.

---

# Recommendations

## For Security Teams

- Do not assume session revocation terminates active Teams remote control sessions.
    
- Review active meetings during incident response.
    
- Remove compromised users from meetings where possible.
    
- Consider disabling Teams remote control if not operationally required.
    
- Update incident response procedures to include meeting termination validation.
    

## For Microsoft

- Consider binding remote control authorization to ongoing authentication state.
    
- Consider terminating active remote control sessions when account revocation occurs.
    
- Provide administrators with visibility into active remote control relationships.
    

---

# Conclusion

Microsoft Entra ID session revocation successfully prevents new Teams interactions from being established.

However, based on testing, existing Teams remote control sessions may continue operating after revocation has occurred.

While this behavior does not constitute an authentication bypass, it may create a gap between expected containment and actual containment during incident response operations.

Organizations should evaluate whether Teams remote control is necessary within their environment and consider disabling the feature if the associated risk outweighs its operational benefits.

---

## References

Microsoft Teams Meeting Policy Documentation

[https://learn.microsoft.com/en-us/MicrosoftTeams/meeting-who-present-request-control](https://learn.microsoft.com/en-us/MicrosoftTeams/meeting-who-present-request-control)

Microsoft Teams Content Sharing Documentation

[https://support.microsoft.com/en-us/office/share-content-in-a-meeting-in-teams-fcc2bf59-aecd-4481-8f99-ce55dd836ce8](https://support.microsoft.com/en-us/office/share-content-in-a-meeting-in-teams-fcc2bf59-aecd-4481-8f99-ce55dd836ce8)

Microsoft Teams Meeting Roles

[https://support.microsoft.com/en-us/teams/meetings/roles-in-microsoft-teams-meetings](https://support.microsoft.com/en-us/teams/meetings/roles-in-microsoft-teams-meetings)

---

## Proof of Concept

A proof-of-concept video demonstrating the behavior described in this research is available in this repository.
