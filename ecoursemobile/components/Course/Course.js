import { View, Text, ActivityIndicator, Image , ScrollView} from "react-native"
import MyStyles from "../../styles/MyStyles"
import APIs, { endpoints } from "../../configs/APIs"
import React from "react"
import { Chip, List, Searchbar } from "react-native-paper";
import moment from "moment";
import "moment/locale/vi";

const Course = ()   => {
    const [categories, setCategories] = React.useState(null);
    const [courses, setCourses] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const [q, setQ] = React.useState("");
    const [cate_Id, setCate_Id] = React.useState("");

    const loadCates = async () => {
        try {
            let res = await APIs.get(endpoints['categories']);
            setCategories(res.data);
        } catch (ex) {
            console.error(ex);
        }
    }

    const loadCourses = async () => {
        try {
            setLoading(true);
            let url = `${endpoints['courses']}?q=${q}&category_id=${cate_Id}`;
            let res = await APIs.get(url);
            setCourses(res.data.results);
        } catch (ex) {
            console.error(ex);
        }finally{
            setLoading(false);
        }
    }


    React.useEffect(() => {
        loadCates();
    }, []);


    React.useEffect(() => {
        loadCourses();
    }, [q,cate_Id]);


    return (
        <View style={[MyStyles.container, MyStyles.margin]}>
            <Text style={MyStyles.subject}>DANH MỤC CÁC KHÓA HỌC</Text>
            <View style={[MyStyles.row, MyStyles.wrap]}>
                <Chip mode={!cate_Id?"outlined":"flat"} onPress={()=> setCate_Id("")} icon="shape-outline">Tất cả</Chip>
                {categories===null?<ActivityIndicator />:<>
                {categories.map(c => <Chip style={MyStyles.margin} mode={c.id===cate_Id?"outlined":"flat"} onPress={()=> setCate_Id(c.id)} key={c.id} icon="shape-outline">{c.name}</Chip>)}
                </>} 
            </View> 
            <View>
                <Searchbar placeholder="Tìm kiếm khóa học" value={q} onChangeText={setQ} />
            </View>
            <View style={MyStyles.row}>
            <ScrollView>
                {courses.map(c => <List.Item style={MyStyles.margin} key={c.id} title={c.subject} description={moment(c.created_date).fromNow()} left={()=> <Image style={MyStyles.avatar} source={{uri: c.image}} />}   />)}
                {loading && <ActivityIndicator />}
            </ScrollView>
            </View>
        </View>



    )
}

export default Course;