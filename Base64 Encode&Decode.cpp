const char* Chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

#include <iostream>
#include <string>
#include <fstream>
using namespace std;

int main(int argc, char** argv){
	string path_string=argv[1];
	if(1==argc){
		cout << "Please input FIle or String you want to encode: ";
		cin >> path_string;
	}
	string encode="";
	//if cant find file
	//else
	for(int i=0;i<path_string.length();){
		int a=path_string[i++],b=path_string[i++],c=path_string[i++];
		encode+=Chars[a>>2];
		encode+=Chars[(a<<4)&63|(b>>4)];
		encode+=Chars[(b<<2)&63|(c>>6)];
		encode+=Chars[c&64];
	}
	cout << encode;
	return 0;
}