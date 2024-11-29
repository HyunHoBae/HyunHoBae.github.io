class Node{
    constructor(value) {
        this.value = value;   // 값
        this.left = null  // 왼쪽 자식
        this.right= null  //오른쪽 자식
    }


    insert(value){
        let newNode = new Node(value);  //추가 할 새 노드
        if(this.root === null){ // ROOT 노드가 비어 있으면 생성
            this.root = newNode //루트가 비어 있으면 대체 - value Null로 처음에 생성했을수 있음
        }else{
            this.insertNode(this.root, newNode)
        }


    }

    /**
     * 기본 적으로 부모보다 작으면 왼쪽
     * @param node
     * @param newNode
     */
    insertNode(node,newNode) {
        if (newNode.value < node.value) {// 새 노드 값이 기존 노드 보다 작으면
            if (node.left === null) { //기존 노드의 왼쪽이 비어 있다면
                node.left = newNode
            }else{//기존 노드보다 작고 기존 노드의 왼쪽이 비어있지 않으면 왼쪽 노드의 자식으로 삽입
                this.insertNode(node.left,newNode)
            }
        }else{// 새 노드 값이 기존 노드보다 크면
            if (node.right === null) { //기존 노드의 오른쪽이 비어 있다면
                node.right = newNode
            }else{//기존 노드보다 크고 기존 노드의 오른쪽이 비어있지 않으면 오른쪽 노드의 자식으로 삽입
                this.insertNode(node.right,newNode)
            }
        }
    }


    remove(value){
        this.root = removeNode(this.root,value)
    }


    /**
     * 루트 노드 부터 삭제할 노드를 찾아나가고
     * 삭제 후 삭제한 노드의 하위 트리를 본 트리에 연결
     * @param node
     * @param value
     */
    removeNode(node,value){
        if(node === null) return // node가 비어있는 경우 null
        // 1.삭제할 노드 탐색
        if(value < node.value){//삭제 할 노드가 현재 값 보다 작은 경우 왼쪽 탐색
            node.left = this.removeNode(node.left,value);
        }else if(value > node.value){//삭제할 노드가 현재 값 보다 큰 경우 오른쪽 탐색
            node.right = this.removeNode(node.right , value);
        }
        else{ // 현재 노드 == 삭제할 노드
            //2 삭제 및 연결
            if(node.left ===null && node.right ===null){//자식이 없는 경우 null
                return null;
            }

            if(node.left === null){//한쪽만 있는 경우(오른쪽) 그대로 연결
                return node.right;
            }else if(node.right ===null){//한쪽만 있는 경우(왼쪽) 그대로 연결
                return node.left;
            }else{// 양쪽 다 있는 경우
                /*
                오른쪽 노드의 최소값을 삭제되는 노드의 자리에 넣고
                최소값을 제거
                오른쪽 최소값은 오른쪽 보다는 크고 나머지 보다는 작기 때문에 트리의 조건을 만족함
                 */
                let aux = this.findMinNode(node.right);
                node.value = aux;
                node.right = this.removeNode(node.right,aux);
            }

        }
    }

    min(){
        return this.findMinNode(this.root);
    }

    findMinNode(node){// 받은 노드의 최하단 맨 왼쪽이 최소값
        if(node){
            while(node && node.left !== null){
                node= node.left;
            }
        }
        return node;
    }

    max(){
        return this.findMaxNode(this.root)
    }

    findMaxNode(node){// 받은 노드의 최하단 맨 오른쪽이 최소값
        if(node){
            while(node && node.right !== null){
                node= node.right;
            }
        }
        return node;
    }

    search(value){
        return this.searchNode(this.root,value);
    }

    searchNode(node,key){
        if(node ===null) return null;
        if( value<node.value){
            return this.searchNode(node.left,value);
        }else if( value > node.value){
            return this.searchNode(node.right,value);
        }else{
            return node;
        }
    }

}

