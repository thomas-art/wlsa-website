/*
def requestXiaobao(link, cookie):
    try:
        req = requests.get(link, headers={
            "User-Agent": userAgent,
            "Cookies": "SessionId=" + cookie
        })
        data = req.json()
        if "data" not in data:
            raise Exception("unauthorized")
        return req.json()
    except Exception as e:
        print("getInfo error:", e)
        return
*/
let apiMap = {
    GetCurrentStudentInfo: "MemberShip",
    GetCurrentOrgConfigByOrg: "MemberShip",
    GetSchoolSemesters: "School",
    ContinueAnswerForLearningtask: "LearningTask",
    GetStuSubjectListForSelect: "LearningTask",
    GetStuLearningTaskTypeListForSelect: "LearningTask",
    GetList: "LearningTask"
}

async function requestXiaobao(api, options = {}) {
    let strOpts = "";
    for (let key in options) strOpts += `${key}=${options[key]}&`;
    let link = `https://wlsastu.schoolis.cn/api/${apiMap[api]}/${api}?${strOpts}`;
    try {
        const req = await fetch("/wlsash/api/xb?link=" + encodeURIComponent(link));
        let json = await req.text();
        console.log(json);
        json = JSON.parse(json);
        if (!json.data) throw new Error("unauthorized");
        return json.data;
    } catch (e) {
        console.error(e);
        return {};
    }
}
async function getInfo() {
    return await requestXiaobao("GetStudentInfo")
}
async function getOrg() {
    return await requestXiaobao("GetCurrentOrgConfigByOrg")
}
async function getSemesters() {
    return await requestXiaobao("GetSchoolSemesters")
}
async function continueAnswerForLearningtask() {
    return await requestXiaobao("ContinueAnswerForLearningtask")
}
async function getSubjects(semester) {
    return await requestXiaobao("GetStuSubjectListForSelect", {semesterId: semester})
}
async function getTaskTypes(semester) {
    return await requestXiaobao("GetStuLearningTaskTypeListForSelect", {semesterId: semester})
}
async function getList(semester, count) {
    return await requestXiaobao("GetList", {
        semesterId: semester,
        subjectId: null,
        typeId: null,
        key: "",
        mode: null,
        pageIndex: 1,
        beginTime: "2024-08-01",
        endTime: "2025-12-31",
        pageSize: count
    })
    //?semesterId=28043&subjectId=null&typeId=null&key=&beginTime=2024-08-01&endTime=2025-02-20&mode=null&pageIndex=1&pageSize=12
}