# Contribution
## Setup Environment
### Prerequisite
- Nodejs version: `>=16` or `14.13` or `12.22`
- Installed Harvester version: `>=v1.0.0`

```bash
npm ci  # install dependencies
mv cypress.env.json.example cypress.env.json
vim cypress.env.json  # update relevant variables accordingly
```

## Develop
```bash
npx cypress open
```

## Execute Test Cases
```bash
npx cypress run
```


# Convention
## Frontend test skeletons <a name="test_skeletons">

Frontend tests are done in [Cypress](https://cypress.io). Code is located at [`cypress`](cypress/). The test cases are in [`cypress/testcases`](cypress/testcases/). The way that they are organized are in `describe` and `it` blocks. Cypress uses [Mocha](https://mochajs.org/) to do [BDD](https://en.wikipedia.org/wiki/Behavior-driven_development). An `it` block is a test case, and a `describe` block it a suite of tests with `it` blocks inside of it. 

The test skeleton is just a stub method with JSDoc comments that add steps. Here's an example of a test skeleton for logging in. You would put this in the appropriate test spec in [`cypress/testcases`](cypress/testcases/). For login it would be [`login.spec.ts`](cypress/testcases/login.spec.ts). Since it's not implemented you will also add the `notImplemented` tag. 
```typescript
/**
* 1. Load login page
* 2. Enter in username and password
* 3. Click Login
* 4. Verify that the dashboard loads
* @notImplemented
*/
export function loginTest() {}
```
It's worth noting that this function and docs can't be inside of a `describe` or `it` block for them to show correctly in our static site generator.

The test skel does not include the `describe` or `it` block, but here's an example of a fully implemented test spec with just an `it` block from [settings.spec.ts](cypress/testcases/settings.spec.ts)
```typescript
/**
 * 1. Login
 * 2. Navigate to the Advanced Settings Page via the sidebar
 */
export function navigateAdvanceSettingsPage() {};
it('should navigate to the Advanced Settings Page', () => {
    login.login();
    sidebar.advancedSettings();
});
```

Here's an example with a `describe` block from [login.spec.ts](cypress/testcases/login.spec.ts)
```typescript
/**
 * This is the login spec
 * 1. Login for first time
 * 2. Login with already set password
 */
describe('login page for harvester', () => {
    it('should login the first time', () => {
        const login = new LoginPage();
        login.firstLogin();
    });
    
    it('should login successfully', () => {
        const login = new LoginPage();
        login.login();
    });
});
```

Here's an example with both a `describe` and an `it` block from [support.spec.ts](cypress/testcases/support.spec.ts)

```typescript
/**
 * 1. Login
 * 2. Navigate to the support page
 * 3. Validate the URL
 */
export function checkSupportPage() {}
describe('Support Page', () => {
    it('Check suport page', () => {
        login.login();
        support.visitSupportPage();
    });
});

/**
 * 1. Login
 * 2. Navigate to the support page
 * 3. Click Generate Support Bundle
 * 4. Input Description
 * 5. Click Generate
 * 6. Wait for download
 * 7. Verify Downlaod
 * @notImplementedFully
 */
export function generateSupportBundle() {}
it('Generate Support Bundle', () => {
    login.login();
    support.generateSupportBundle('this ia a test description');
});

```

## How to use docker image

### Build docker image

```bash
docker build . -t harvester/cypress-e2e
```

### Run docker image

The following environment variables are required to run the docker image:
- `MINIO_ENDPOINT`: The endpoint of the minio server
- `MINIO_ACCESS_KEY`: The access key of the minio server
- `MINIO_SECRET_KEY`: The secret key of the minio server

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cypress-e2e
  namespace: harvester
spec:
  template:
    spec:
      containers:
      - env:
        - name: MINIO_ENDPOINT
          value: 
        - name: MINIO_ACCESS_KEY
          value: 
        - name: MINIO_SECRET_KEY
          value: 
        image: harvester/cypress-e2e
        imagePullPolicy: Always
        name: container-0
        volumeMounts:
        - mountPath: /tests/cypress/cypress.env.json
          name: vol-e2e
          subPath: cypress.env.json
      volumes:
      - configMap:
          defaultMode: 420
          name: cypress-config
        name: vol-e2e
```

```YAML
apiVersion: v1
data:
  cypress.env.json: |-
    {
      "username": "admin",
      "password": "password1234",
      "baseUrl":  "https://192.0.0.1",
    }
kind: ConfigMap
metadata:
  name: cypress-config
  namespace: harvester

```


### View the test result

The docker image will automatically run cypress test and upload the test result to the minio server.
The default bucket name is `cypress-test-report`, and the default dir path is `cypress/results/`.

You can view the test result by clicking [here](https://minio.provo.rancherlabs.com:31524/cypress-test-report/index.html) for or using the following command:

```bash
./scripts/list-reporters
```
