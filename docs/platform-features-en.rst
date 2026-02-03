Lab Platform Features
=====================

This document explains the main features and configuration capabilities of the lab platform for managing virtual labs and workshops.

**Key Features:**

- **maximum:** Set the total capacity of the portal (maximum number of active sessions).
- **capacity:** Define the capacity for each individual workshop.
- **reserved:** Number of pre-launched/standby instances for each scenario to speed up user session loading. The sum of reserved and running scenarios cannot exceed the maximum.
- **initial:** The number of instances created at the start of an event or workshop, based on expected audience size. Unlike reserved, initial is for immediate availability upon the start. If `initial < reserved`, only the reserved number is created. If `initial` is zero, nothing is pre-created; new sessions will be started as users arrive. If higher, initial number is created first, then the reserved ones keep being maintained.
- **labels:** Helps to tag both the portal and scenarios for filtering or API queries (e.g., scenario difficulty, user type, or other metadata).
- **registered:** Sets the limit for the number of concurrent scenarios each registered user can run.
- **anonymous:** The limit for the number of concurrent scenarios for anonymous users.
- **expires:** Sets the scenario session timeout (in seconds, minutes, or hours). At the end of this period, the session is automatically deleted. Future improvements may include auto-snapshotting unfinished sessions.
- **orphaned:** If a session is abandoned (no active usage), it will be closed and deleted after a specified period, optimizing resource usage.
- **deadline:** The absolute maximum total time for a scenario, including all extensions a user may request.
- **overtime:** Allows the user to add extra time to their scenario session when it’s almost up (e.g., each click adds 25% more time by default, but this can be customized). Only available once the session timer turns orange (near deadline).
- **overdue:** If a scenario takes too long to load, this controls the max wait time. If exceeded, the scenario is killed and recreated—useful for SLO and preventing user frustration.
- **updates.workshop=true:** Replaces old workshops with newer versions automatically. Existing sessions aren’t deleted; users can finish their labs even after a workshop update. When all active sessions end, only the new workshop version is available.
- **workshop.defaults.refresh:** Regularly refreshes workshop environments based on a schedule. If active sessions exist from the old environment, the system waits for them to finish before completing the refresh, ensuring optimal resource management.

---

### Example Feature Explanation

**reserved:**  
Defines how many scenario instances are always kept ready in standby mode, ensuring new users start their labs without long wait times. These reserved sessions are pre-allocated but not actively in use until a user starts a session. The total of reserved and running sessions must not exceed the value set for **maximum**.

---

### Feature Usage Notes

- Combine **initial** and **reserved** for flexible and optimized resource allocation. For example, set a high initial value for anticipated events or workshops, then maintain a steady reserved count for regular operation.
- Use **labels** to categorize scenarios (e.g., "Beginner", "DevOps", "Security") and enable advanced filtering in the dashboard or through APIs.
- Set **expires** and **deadline** to balance resource optimization with a good user experience—expired or abandoned sessions are cleaned up automatically.
- Leverage **overtime** and **overdue** to keep lab environments responsive but fair, allowing users to extend time when needed and minimizing resource deadlocks.
- **updates.workshop=true** ensures the platform always runs the most up-to-date workshop version without interrupting current users.
- Employ **workshop.defaults.refresh** for automated cleanup and to prevent stale environments from consuming resources.

---

## Best Practices

- Always set proper limits for **maximum**, **capacity**, **reserved**, and **overtime** based on your infrastructure capabilities and expected lab usage patterns.
- Regularly review and adjust **expires**, **orphaned**, and **deadline** settings to ensure a balance between user flexibility and system performance.
- Utilize **labels** for both technical (e.g., required resources, operating system) and learning purposes (e.g., scenario difficulty).

---

## Summary

The above platform features enable fine-grained control and optimization of lab delivery and management for both instructors and technical administrators. Continually review and tailor these options as your user base and scenario complexity grow.

---

For questions or improvement requests related to these platform features, please contact the platform administrator or refer to the official documentation.
