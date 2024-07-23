#include <bits/stdc++.h>
using namespace std;

#define forz(i,a,b) for(ll i = a;i<b;i++)
#define ll long long

ll mx = 0;

struct Node{
    Node* left;
    Node* right;

    ll val; // The byte that is compressed

    Node(ll value){
        left = NULL;
        right = NULL;
        val = value;
    }
};

void dfs(Node* ptr,string &st,map<ll,string> &encoding){
    if (ptr != NULL){

        if ((ptr->val) != mx+1){
            encoding[ptr->val] = st;
        }

        st.push_back('0');
        dfs(ptr->left,st,encoding);
        st.pop_back();

        st.push_back('1');
        dfs(ptr->right,st,encoding);
        st.pop_back();
    }
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    freopen("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\lzw_comp.txt","r", stdin);
    freopen("C:\\Users\\Admin\\Desktop\\Codeforces\\SIH\\ZSTD\\hoffmann_comp.txt","w", stdout);

    ll n;
    cin>>n;

    vector<ll> v(n);
    map<ll,ll> cnt; // Stores the count of each node.

    forz(i,0,n){
        cin>>v[i];
        cnt[v[i]]++;
        mx = max(mx,v[i]);
    }

    set<pair<ll,Node*>> freq; // { frequency, node ptr }

    for(auto i:cnt){
        freq.insert({i.second,new Node(i.first)});
    }

    while (freq.size()>1){
        auto [c1,p1] = *freq.begin();
        freq.erase(freq.begin());

        auto [c2,p2] = *freq.begin();
        freq.erase(freq.begin());

        auto ptr = new Node(mx+1);
        ptr->left = p1;
        ptr->right = p2;

        freq.insert({c1+c2,ptr});
    }

    auto [total_c,root] = *freq.begin();
    map<ll,string> encoding;
    string st = "";

    dfs(root,st,encoding);

    // cout<<encoding.size()<<'\n';
    // for(auto [val,cval]: encoding){
    //     cout<<val<<' '<<cval<<'\n';
    // }

    forz(i,0,n){
        cout<<encoding[v[i]];
    }

    return 0;
}

// ------------------------------------------------ BY SHRI ---------------------------------------------------- //