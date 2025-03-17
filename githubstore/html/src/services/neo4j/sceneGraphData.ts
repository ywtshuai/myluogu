/**
 * @file 场景图数据初始化
 * @description 初始化 Neo4j 数据库中的场景图数据
 */
import { neo4jService } from './neo4jService';

// 场景节点类型
enum SceneType {
  TOWN = 1,
  BUILDING = 2,
  ROOM = 3,
  AREA = 4,
  OBJECT = 5
}

// 初始化场景图数据
export async function initializeSceneGraph(): Promise<void> {
  try {
    // 如果服务处于模拟模式，直接返回
    if ((neo4jService as any).mockMode === true) {
      console.log('模拟模式：跳过场景图初始化');
      return;
    }
    
    // 检查是否已有数据
    const hasData = await neo4jService.hasSceneData();
    
    // 如果已有节点数据，则不重新初始化
    if (hasData) {
      console.log('场景图数据已存在，跳过初始化');
      return;
    }
    
    console.log('开始初始化场景图数据...');
    
    // 清空现有数据
    await neo4jService.executeQuery('MATCH (n) DETACH DELETE n');
    
    // 创建场景节点
    const createSceneNodes = `
      // 创建城镇
      CREATE (town:Scene {id: 'town1', name: '落叶镇', type: ${SceneType.TOWN}, description: '一个宁静的小镇，四周被茂密的森林环绕'})
      
      // 创建建筑
      CREATE (inn:Scene {id: 'inn1', name: '醉鹿旅店', type: ${SceneType.BUILDING}, description: '镇上最受欢迎的旅店，以其美味的蜜酒和舒适的床铺闻名'})
      CREATE (blacksmith:Scene {id: 'blacksmith1', name: '铁匠铺', type: ${SceneType.BUILDING}, description: '烟雾缭绕的铁匠铺，叮叮当当的敲击声不绝于耳'})
      CREATE (market:Scene {id: 'market1', name: '集市', type: ${SceneType.BUILDING}, description: '热闹的集市，各种商品琳琅满目'})
      CREATE (temple:Scene {id: 'temple1', name: '光明神殿', type: ${SceneType.BUILDING}, description: '庄严肃穆的神殿，供奉着光明之神'})
      
      // 旅店内的房间
      CREATE (bar:Scene {id: 'bar1', name: '酒吧', type: ${SceneType.ROOM}, description: '温暖的酒吧，壁炉里的火焰噼啪作响'})
      CREATE (kitchen:Scene {id: 'kitchen1', name: '厨房', type: ${SceneType.ROOM}, description: '忙碌的厨房，香气四溢'})
      CREATE (innRoom1:Scene {id: 'innRoom1', name: '客房1', type: ${SceneType.ROOM}, description: '舒适的客房，有一张柔软的床'})
      CREATE (innRoom2:Scene {id: 'innRoom2', name: '客房2', type: ${SceneType.ROOM}, description: '豪华的客房，配有私人浴室'})
      
      // 铁匠铺内的区域
      CREATE (forge:Scene {id: 'forge1', name: '锻造间', type: ${SceneType.ROOM}, description: '炽热的锻造间，火炉熊熊燃烧'})
      CREATE (storage:Scene {id: 'storage1', name: '仓库', type: ${SceneType.ROOM}, description: '堆满武器和材料的仓库'})
      
      // 集市内的摊位
      CREATE (foodStall:Scene {id: 'foodStall1', name: '食品摊', type: ${SceneType.AREA}, description: '香气四溢的食品摊，出售各种美食'})
      CREATE (weaponStall:Scene {id: 'weaponStall1', name: '武器摊', type: ${SceneType.AREA}, description: '陈列着各种武器的摊位'})
      CREATE (potionStall:Scene {id: 'potionStall1', name: '药水摊', type: ${SceneType.AREA}, description: '摆满五颜六色药水的摊位'})
      
      // 神殿内的区域
      CREATE (altar:Scene {id: 'altar1', name: '祭坛', type: ${SceneType.AREA}, description: '神圣的祭坛，供奉着光明神像'})
      CREATE (library:Scene {id: 'library1', name: '图书馆', type: ${SceneType.ROOM}, description: '收藏着古老典籍的图书馆'})
      
      // 酒吧内的物品
      CREATE (counter:Scene {id: 'counter1', name: '吧台', type: ${SceneType.OBJECT}, description: '光滑的木质吧台，上面摆满了酒瓶'})
      CREATE (fireplace:Scene {id: 'fireplace1', name: '壁炉', type: ${SceneType.OBJECT}, description: '温暖的石砌壁炉，火焰跳动'})
      CREATE (table1:Scene {id: 'table1', name: '桌子1', type: ${SceneType.OBJECT}, description: '一张结实的木桌，周围有几把椅子'})
      CREATE (table2:Scene {id: 'table2', name: '桌子2', type: ${SceneType.OBJECT}, description: '角落里的小桌子，适合私密交谈'})
      
      // 建立关系
      CREATE (town)-[:CONTAINS]->(inn)
      CREATE (town)-[:CONTAINS]->(blacksmith)
      CREATE (town)-[:CONTAINS]->(market)
      CREATE (town)-[:CONTAINS]->(temple)
      
      CREATE (inn)-[:CONTAINS]->(bar)
      CREATE (inn)-[:CONTAINS]->(kitchen)
      CREATE (inn)-[:CONTAINS]->(innRoom1)
      CREATE (inn)-[:CONTAINS]->(innRoom2)
      
      CREATE (blacksmith)-[:CONTAINS]->(forge)
      CREATE (blacksmith)-[:CONTAINS]->(storage)
      
      CREATE (market)-[:CONTAINS]->(foodStall)
      CREATE (market)-[:CONTAINS]->(weaponStall)
      CREATE (market)-[:CONTAINS]->(potionStall)
      
      CREATE (temple)-[:CONTAINS]->(altar)
      CREATE (temple)-[:CONTAINS]->(library)
      
      CREATE (bar)-[:CONTAINS]->(counter)
      CREATE (bar)-[:CONTAINS]->(fireplace)
      CREATE (bar)-[:CONTAINS]->(table1)
      CREATE (bar)-[:CONTAINS]->(table2)
    `;
    
    await neo4jService.executeQuery(createSceneNodes);
    console.log('场景图数据初始化成功');
  } catch (error) {
    console.error('场景图数据初始化失败:', error);
    // 不抛出错误，允许应用继续运行
  }
} 