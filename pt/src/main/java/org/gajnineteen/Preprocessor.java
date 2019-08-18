package org.gajnineteen;
import org.gajnineteen.processor.impl.LRProcessor;
import java.io.*;

public class Preprocessor {

    /**
     *  LRProcessor 预处理步骤
     *  1. 从bug报告中提取summary+description
     *  2. 按capital letters断开复合词，原来的也保留
     *  3. 移除标点，数字，标准IR停用词(NLTK stopwords list)
     *  4. use Porter stemmer to stemize words
     */
    public static void doProcess(String source_path,String target_path) throws IOException {
        LRProcessor lrp = new LRProcessor();

        File file = new File(source_path);		//获取其file对象
        File[] dirs = file.listFiles();	//遍历path下的文件和目录，放在File数组中

        BufferedReader in = null ;
        BufferedWriter out= null ;
        for(File dir:dirs){					//遍历File[]数组
            if(dir.isDirectory()) {
                File[] files = dir.listFiles();
                String projectPath = target_path + "/" + dir.getName() ;
                createDir(projectPath);

                for(File f : files) {
                    if (!f.isDirectory() && !f.getName().equals(".DS_Store")) {
                        String file_path = f.getPath();
                        String file_name = f.getName();
//                        System.out.println(file_path);


                        //读取文件(字符流)
                        in = new BufferedReader(new InputStreamReader(new FileInputStream(file_path), "utf-8"));
                        String toFilePath = target_path + "/" + dir.getName() + "/"+ file_name ;
//                        System.out.println(filePath);
                        createFile(toFilePath);

                        //写入相应的文件
                        out = new BufferedWriter(new OutputStreamWriter
                                (new FileOutputStream(toFilePath), "utf-8"));
                        //读取数据
                        //循环取出数据
                        String str = null;
                        while ((str = in.readLine()) != null) {
//                    System.out.println(str);
                            lrp.setText(str);
                            String result = lrp.process();
//                    System.out.println(result);
                            out.write(result);
                            out.newLine();
                        }
                        //清除缓存
                        out.flush();

                    }
                }
            }
        }
        //关闭流
        in.close();
        out.close();
    }

//    public static void main(String[] args) throws IOException {
//        String source_path = "raw_br";		//要遍历的路径
//        String target_path = "preprocessed_br" ;
//        Preprocessor.doProcess(source_path,target_path);
//    }


    public static void main(String[] args) throws IOException {
//        String source_dir = "total_raw_br_0804" ;
//
//        String target_dir = "raw_br_0810" ;
//
//        fromTotal2Raw(source_dir,target_dir);

        String source_path = "/Users/lienming/Downloads/istDat4exp/bugReport4Vector";		//要遍历的路径
        String target_path = "/Users/lienming/Downloads/istDat4exp/preprocessed_bugReport4Vector" ;
        Preprocessor.doProcess(source_path,target_path);

    }



    static void createDir(String path) {
        File dir = new File(path);
        if(!dir.exists()){
            dir.mkdirs();
        }
    }

    static void createFile(String path)  {
        File dir = new File(path);

        if(!dir.exists()){
            try {
                dir.createNewFile();
            } catch (IOException e) {
                System.out.println(path);
                e.printStackTrace();
            }
        }
    }

    static void writeToFile(String path, String title, String desc) throws IOException {
        BufferedWriter out = new BufferedWriter(new OutputStreamWriter
                (new FileOutputStream(path),
                        "utf-8"));
        out.write(title);
        out.newLine();
        out.write(desc);
        out.flush();
        out.close();
    }

//      sublime text \t 有问题
    public static void fromTotal2Raw(String source_dir, String target_dir) throws IOException {
        String[] source_paths = {"Closure","Lang","Math"};  // ,"Mockito","Time"
        BufferedReader in = null ;
        BufferedWriter out = null ;

        for(String source_path : source_paths) {
            String str = null ;
            File file = new File(source_dir+"/"+source_path);
            String file_path = file.getPath();
            in = new BufferedReader(new InputStreamReader(new FileInputStream(file_path), "utf-8"));

            String rawProjectPath = target_dir+"/"+source_path;
            createDir(rawProjectPath);

            while ((str = in.readLine()) != null) {
                String[] br = str.split("\t");
                String br_id;
                String bug_id;
                String br_title;
                String br_desc;
                if(source_path.equals("Math")){  // 0,4,5,6
                    br_id  = br[0];
                    bug_id = br[4];
                    br_title = br[5];
                    br_desc = br[6];
                } else  {  //others: A,E,G,H - 0,4,6,7
                    br_id  = br[0];
                    bug_id = br[4];
                    br_title = br[6];
                    br_desc = br[7];
                }
//                System.out.println(br_id);
//                System.out.println(bug_id);
//                System.out.println(br_title);
//                System.out.println(br_desc);
//                System.out.println();

                String rawFilePath = target_dir+"/"+source_path+"/"+ source_path +"_"+br_id ;
                createFile(rawFilePath);

                writeToFile(rawFilePath, br_title, br_desc );
            }

        }

        //for "Mockito" ,"Time"
        String[] source_paths_2 = {"Mockito","Time"};

        for(String source_path : source_paths_2) {
            String str = null ;
            String file_path = source_dir+"/"+source_path ;
            in = new BufferedReader(new InputStreamReader(new FileInputStream(file_path), "utf-8"));

            String rawProjectPath = target_dir+"/"+source_path;
            createDir(rawProjectPath);

            int count = 0;
            String total_str = null;
            while ((str = in.readLine()) != null) {
//                System.out.println(count);
//                System.out.println(str);
                if(str.startsWith(""+(1+count)+"\t")) {
                    if (count == 0) {
                        count = 1;
                        total_str = str;
                        continue;
                    } else {
                        //do split for total_str
//                        System.out.println(total_str);
                        String[] br = total_str.split("\t");

//                        System.out.println("size:"+br.length);
                        String br_id;
                        String bug_id;
                        String br_title;
                        String br_desc;
                        if(source_path.equals("Time")) {
                            //0,5,7,8
                            br_id = br[0];
                            bug_id = br[5];
                            br_title = br[7];
                            br_desc = br[8];
                        } else {
                            br_id  = br[0];
                            bug_id = br[4];
                            br_title = br[6];
                            br_desc = br[7];
                        }

//                            System.out.println(br_id);
//                            System.out.println(bug_id);
//                            System.out.println(br_title);
//                            System.out.println(br_desc);
//                            System.out.println();

                        String rawFilePath = target_dir+"/"+source_path+"/"+ source_path +"_"+br_id ;
                        createFile(rawFilePath);

                        writeToFile(rawFilePath, br_title, br_desc );

                        total_str = str;
                        count++;
                    }
                } else {
                    total_str = total_str+"\n"+str;
//                    System.out.println(total_str);
                }


            }
        }

//        in.close();
//        out.close();
    }

}



